# PCA Flylets: Invariant Risk Metrics
Replicating the work from *PCA: Invariant Risk Metrics and Representation of Residuals for Bond Returns* [SSRN Link](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2777026)

# Background
The paper which won the 2016 Risk.net buy-side quants of the year. The idea behind the paper is to develop a framework for finding sensitivities within the PCA-based space for interest rate derivatives. The main idea behind PCs is to find orthogonal vectors to the 2nd principal component for the local sensitivies. This codebase using data collected from Bloomberg with Treasury, Swaps, and ATM Swaption rates to find flylets. The flylets are unique to themselves and do not follow the 1x2x1 standard weighting. 

# Data
First begin with the data. I was not able to find more historical Swaption data available on Bloomberg. 
![image](https://github.com/diegodalvarez/PCAFlylet/assets/48641554/f7d81cf3-8492-4c88-8018-21c15bfa2ecb)
Then we can construct the various curves for each type 
![image](https://github.com/diegodalvarez/PCAFlylet/assets/48641554/eab94b57-8e28-4d64-9208-b292a5f34ab0)

# Calculating Flylet Weight
In this case I've calculated flylet weight by finding orthogonal vectors in the L2 norm for specific tenors. Knowing that of the vectors of tenors per each PC will be zeroed when calculating hte flylet we can essentially cross the first two PCs of 3 dimensions with the respective tenors. I've doubled check that the flylets are orthogonal to the PCs and in the L2 norm. 
![image](https://github.com/diegodalvarez/PCAFlylet/assets/48641554/41fc6322-11e8-4563-82db-b660ace29245)
![image](https://github.com/diegodalvarez/PCAFlylet/assets/48641554/36965cf4-2a06-410f-ace1-e878c144040c)
Of course I do not expect exact orthogonality when constructing these vectors but the results are enough for me be sure that these vectors are orthogonal. Although I'd admit the weighting that I found for these vectors are less (in absolute) terms than what the authors had found which I am a bit concerned with. 
Below are the weights of specific flylets
![image](https://github.com/diegodalvarez/PCAFlylet/assets/48641554/15f43b80-d006-48fb-b629-35ac0a55ee10)
