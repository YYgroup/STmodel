# STmodel
A predictive model of the turbulent burning velocity for planar and Bunsen flames over a wide range of conditions

Model predictions on turbulent burning velocity of lean hydrogen flames at different pressures, with DNS data from [Lu & Yang, 2020](https://doi.org/10.1016/j.proci.2020.06.162)
<p align="center">
<img src="./data/fig/fig_model_st_Lu2020.png" width="360">
</p>

Validation cases:
<p align="center">
<img src="./data/fig/fig_diagram.png" width="560">
</p>

Model predictions for the 285 cases:
<p align="center">
<img src="./data/fig/fig_st_predictions.png" width="360">
</p>

# Dependence
cantera
https://github.com/Cantera/cantera

pyutils
https://github.com/Combustion-Zhen/pyutils

# Get start
Please check the /examples folder

/examples/hydrogen_Lu_2021 contains full procedure to run the model
1. run driver_counterflow.py to get the laminar flame solutions for laminar flame parameters and tabulation
2. run run_model_st.py to get the model predictions and comparisons with data

Note: 
The first run will take some time to do the laminar flame simulations and tabulation for a new condition. 
It depends on the fuel and mechanism employed. 
Then the necessary data are stored in laminar_info.npz and stretch_factor_table.npy files. 
Later calls of the model only take negligible time to do algebraic calculations.

# Cite
Zhen Lu and Yue Yang, A predictive model of the turbulent burning velocity for planar and Bunsen flames over a wide range of conditions, Combustion and Flame, 2021, under review. [arXiv](https://arxiv.org/abs/2103.11337)
