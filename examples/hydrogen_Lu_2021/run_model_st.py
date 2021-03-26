# %%

## load packages
import numpy as np
import pyutils.fig as fg
import STmodel.data.cases as stc
import STmodel.model.st as stm

# %%

## get the case, case file stored in STmodel/data/cases
case = stc.case.CaseSet('Lu_2021')
lr = 1.0

# %%

## points to make model prediction
nx = 50
ur_list = np.linspace(0, 25, num=nx)
sr = np.zeros(nx)

# %%

## select a condition T, p, phi
unburnt = 'T-300_p-10_phi-0.6'
## get the data
d = case.get_case_data(unburnt)
## get the reactant information
r = case.get_reactant(unburnt)
## get the model object
m = stm.Model(r)

for i, ur in enumerate(ur_list):
    # calculate model predicitons
    sr[i] = m.ratio_turbulent_burning_velocity(ur, lr)

# %%

## plot settings
config = fg.PlotConfig('manuscript_single')

# %%

## plot model prediciton and data for comparison

fig, ax = config.get_simple()

ax.errorbar(d.turbulence_intensity,
            d.turbulent_burning_velocity,
            yerr=d.turbulent_burning_velocity_std,
            fmt='o', c='b', mec='k', ms=6, mew=1,
            capsize=3, capthick=1.5, elinewidth=1,
            label='DNS')

ax.plot(ur_list, sr, '-', c='r', label='Model')

ax.set_xlim(0, 21)
ax.set_ylim(0, 40)

ax.set_xticks(np.linspace(0, 20, num=5))
ax.set_yticks(np.linspace(0, 40, num=9))

ax.legend(frameon=False)

ax.text(10, 1,
        'Lu \& Yang, 2021\n'
        +r'H$_2$/Air, $\phi=0.6$')

ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)

ax.set_xlabel(r'$u^\prime/s_L^0$')
ax.set_ylabel(r'$s_T/s_L^0$')

# %%

## save the figure

fig.savefig('fig_model_st_Lu2021.png', dpi=400)

# %%
