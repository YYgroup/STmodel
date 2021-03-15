# %%

import numpy as np
import pyutils.fig as fg
import pyutils.ctutils.flame as ctf
import STmodel.data.cases as stc
import STmodel.model.st as stm
import STmodel.model.stuq as stu

# %%

file_uq = 'T-300_p-10_phi-0.6/UQ/counterflow_premixed_all.dat'
data_uq = np.genfromtxt(file_uq)

# %%

case = stc.case.CaseSet('Lu_2021')

# %%

nx = 50
ny = 200

ur_list = np.linspace(0.1, 25, num=nx)
lr = 1

sr_list = np.zeros(nx)

sr_ave = np.zeros(nx)
sr_std = np.zeros(nx)

sr_ave_para = np.zeros(nx)
sr_std_para = np.zeros(nx)

sr_ave_chem = np.zeros(nx)
sr_std_chem = np.zeros(nx)

# %%

config = fg.PlotConfig('manuscript_single')

# %%

unburnt = 'T-300_p-10_phi-0.6'
data = case.get_case_data(unburnt)
r = stm.Reactant(unburnt,
                 case.get_fuel_stream(),
                 case.get_oxy_stream(),
                 case.get_mechanism())
m = stm.Model(r)

# %%

Le = r.Le
sigma = r.sigma

fs = ctf.FreeFlameState('{0}/{0}.xml'.format(unburnt),'h2_Burke_n2.cti','H2')
sc0 = fs.consumption_speed()
dl0 = fs.thermal_thickness()

# %%

A_s, B_s, T_s, C_s = stu.sample_params(1000)

# %%
for i, ur in enumerate(ur_list):
    # calculate model predicitons
    sr_list[i] = m.ratio_turbulent_burning_velocity(ur, lr)
    # calculate uncertainty with respect to para
    sr_MC = stu.fwd_params(ur, lr,
                           unburnt,
                           case.get_fuel_stream(),
                           case.get_oxy_stream(),
                           case.get_mechanism(),
                           A_s, B_s, T_s, C_s)

    sr_ave_para[i] = np.average(sr_MC)
    sr_std_para[i] = np.std(sr_MC)

    # calculate uncertainty with respect to chem
    sr_MC = stu.fwd_chem(ur, lr,
                         unburnt,
                         sc0, dl0, Le, sigma,
                         data_uq)

    sr_ave_chem[i] = np.average(sr_MC)
    sr_std_chem[i] = np.std(sr_MC)

    # calculate uncertainty with respect to chem
    sr_MC = stu.fwd_chem_para(ur, lr,
                              unburnt,
                              sc0, dl0, Le, sigma,
                              data_uq,
                              A_s, B_s, T_s, C_s)

    sr_ave[i] = np.average(sr_MC)
    sr_std[i] = np.std(sr_MC)
# %%

fig, ax = config.get_simple()

"""
ax.contourf(ur_list, sr_p, np.flipud(np.rot90(pdf)), 
            cmap='binary', levels=1000,
            vmin=0.0, vmax=0.5)
"""
ax.plot([-20,-10], [-1, -1], '-r', label='Model')

ax.plot(data.turbulence_intensity,
        data.turbulent_burning_velocity,
        ls = '', marker='o', c='b', mec='k')

ax.plot(ur_list, sr_list, '-r')


ax.fill_between(ur_list, sr_ave - 2.0 * sr_std, sr_ave + 2.0 * sr_std,
                color='xkcd:light blue', label=r'$\pm 2\sigma,\;\mathrm{chemistry \& parameters}$')

ax.fill_between(ur_list, sr_ave_chem - 2.0 * sr_std_chem, sr_ave_chem + 2.0 * sr_std_chem,
                color='xkcd:lavender', label=r'$\pm 2\sigma,\;\mathrm{chemistry}$')

ax.fill_between(ur_list, sr_ave_para - 2.0 * sr_std_para, sr_ave_para + 2.0 * sr_std_para,
                color='xkcd:light grey', label=r'$\pm 2\sigma,\;\mathrm{parameters}$')

ax.set_xlim(0, 25)

ax.set_xticks(np.linspace(0, 25, num=6))
#ax.set_yticks(np.linspace(0, 15, num=6))

ax.legend(frameon=False, loc='upper left')

ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)

ax.set_xlabel(r'$u^\prime/s_L^0$')
ax.set_ylabel(r'$s_T/s_L^0$')

# %%

fig.savefig('fig_model_UQ_Lu2021.png', dpi=400)

# %%
