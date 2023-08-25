# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 13:50:46 2023

@author: Diego
"""

import pdblp
import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as web

pd.set_option('display.max_columns', None)

def get_tickers() -> list:

    swap_tickers = (pd.read_csv(
        "swap_tickers.csv",
        index_col = 0).
        assign(swap = lambda x: x.Description.str.split(" ").str[1]).
        query("swap == 'Swap'").
        sort_values("Security").
        assign(tenor = lambda x: x.Description.str.split(" ").str[-1])
        ["Security"].
        drop_duplicates().
        to_list())
    
    swaption_name = (pd.read_csv(
        "swaption_tickers.csv")
        ["Ticker"].
        to_list())
    
    swaption_tickers = ["{} Curncy".format(i) for i in swaption_name]
    output_tickers = swap_tickers + swaption_tickers
    
    return output_tickers

def bbg_collect(years_back: int = 10) -> None:
    
    tickers = get_tickers()
        
    end_date = dt.date.today()
    start_date = dt.date(year = end_date.year - years_back, month = end_date.month, day = end_date.day)
    
    end_date_input  = end_date.strftime("%Y%m%d")
    start_date_input = start_date.strftime("%Y%m%d")
    
    con = pdblp.BCon(debug = False, port = 8194, timeout = 5_000)
    con.start()
    
    print("[INFO] Collecting Data From Bloomberg")
    
    df_tmp = (con.bdh(
        tickers = tickers,
        flds = ["PX_LAST"],
        start_date = start_date_input,
        end_date = end_date_input).
        reset_index().
        melt(id_vars = "date"))
    
    (df_tmp.to_parquet(
        path = "swaps_swaptions.parquet",
        engine = "pyarrow"))
    
    print("[INFO] Saved Data From Bloomberg")
    
def fred_collect(years_back: int = 10) -> None:
    
    end_date = dt.date.today()
    start_date = dt.date(year = end_date.year - years_back, month = end_date.month, day = end_date.day)
    tickers = ["DGS1", "DGS1MO", "DGS3MO", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20"]
    
    df = (web.DataReader(
        name = tickers,
        data_source = "fred",
        start = start_date,
        end = end_date).
        reset_index().
        melt(id_vars = "DATE"))
    
    df.to_parquet(
        path = "tsy.parquet",
        engine = "pyarrow")

def collect():
    bbg_collect()
    fred_collect()

def _clean():        

    fred_df = (pd.read_parquet(
        path = "tsy.parquet",
        engine = "pyarrow").
        assign(source = "fred", sec_type = "treasury").
        rename(columns = {
            "DATE": "date",
            "variable": "ticker"}))
    
    bbg_df = (pd.read_parquet(
        path = "swaps_swaptions.parquet",
        engine = "pyarrow").
        dropna().
        drop(columns = ["field"]).
        assign(
            source = "Bloomberg",
            str_size = lambda x: x.ticker.str.len(),
            sec_type = lambda x: np.where(x.str_size == 15, "swaption", "swap")).
        drop(columns = ["str_size"]))
    
    df_combined = pd.concat([fred_df, bbg_df])
    
    df_combined.to_parquet(
        path = "rates_data.parquet",
        engine = "pyarrow")
    
def clean():
    
    try: 
        _clean()
        
    except:
        collect()
        clean()

if __name__ == "__main__":
    clean()
