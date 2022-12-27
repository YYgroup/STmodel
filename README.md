# STmodel
A predictive model of the turbulent burning velocity for planar and Bunsen flames over a wide range of conditions

Model predictions on turbulent burning velocity of lean hydrogen flames at different pressures, with DNS data from [Lu & Yang, 2021](https://doi.org/10.1016/j.proci.2020.06.162)
<p align="center">
<img src="./data/fig/fig_model_st_Lu2021.png" width="360">
</p>

Validation cases:
<p align="center">
<img src="./data/fig/fig_diagram.png" width="560">
</p>

Model predictions for the 490 cases:
<p align="center">
<img src="./data/fig/fig_st_predictions.png" width="360">
</p>

# Dependence

[pyutils](https://github.com/Combustion-Zhen/pyutils)
a package including interfaces for I/O, plot, and cantera

[cantera](https://cantera.org/), [matplotlib](https://matplotlib.org/), [numpy](https://numpy.org/), [scipy](https://www.scipy.org/)

# Get start
Please check the /examples folder for two cases of hydrogen and methane, comparing between model predictions and DNS results.

steps:
1. run driver_counterflow.py to get the laminar flame solutions for laminar flame parameters and stretch factor tabulation
2. run run_model_st.py/run_model_UQ_para.py to get the model predictions and comparisons with data, you can also check the .ipynb file for notebook.

Note: 
The first run will take some time to do the laminar flame simulations and tabulation for a new condition. 
It depends on the fuel and mechanism employed. 
Then the necessary data are stored in laminar_info.npz and stretch_factor_table.npy files. 
Later calls of the model only take negligible time to do algebraic calculations.

# Refs:

Zhen Lu and Yue Yang, Modeling pressure effects on the turbulent burning velocity for lean hydrogen/air premixed combustion, Proceedings of the Combustion Institute, 38, 2901-2908, 2021. [arXiv](https://arxiv.org/abs/1911.10815) [PCI](https://doi.org/10.1016/j.proci.2020.06.162)

Zhen Lu and Yue Yang, Modeling of the turbulent burning velocity for planar and Bunsen flames over a wide range of conditions, Acta Mechanica Sinica, 38, 121504, 2022. [arXiv](https://arxiv.org/abs/2103.11337) [AMS](https://doi.org/10.1007/s10409-021-09027-3)
