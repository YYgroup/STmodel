# %%
import numpy as np
import pyutils.fig as fg
# %%
file_name = 'counterflow_premixed_all.dat'
data = np.genfromtxt(file_name)
data_shape = data.shape
# %%
pc = fg.PlotConfig('manuscript_single')
# %%
fig, ax = pc.get_simple()

for x, y in zip(data[0::2],data[1::2]):
    ax.plot(x[0], y[1], 'ob', mec='k')
# %%
num = 50
x = np.logspace(-1, 2, num=num)
#y = np.zeros(data[::2].shape)
y = np.array([])
#
for Ka, sc in zip(data[0::2],data[1::2]):
    y = np.append(y, np.interp(x, Ka[1:], sc[1:]/sc[1]))
#
I0 = y.reshape(-1,num)
# %%
I0_ave = I0.mean(axis=0)
I0_std = I0.std(axis=0)
# %%
fig, ax = pc.get_simple()

ax.plot(x, I0_ave, '-r', label=r'$I_0$')
ax.fill_between(x, I0_ave-2*I0_std, I0_ave+2*I0_std,
                color='xkcd:light grey')
ax.fill_between(x, I0_ave-I0_std, I0_ave+I0_std,
                label=r'$I_0\pm \sigma$',
                color='xkcd:grey')

ax.fill_between([0.1,10], [-5,-5], [-4,-4],
                label=r'$I_0\pm 2\sigma$',
                color='xkcd:light grey')

ax.legend(frameon=False, loc='center left')

ax.set_xscale('log')
ax.set_xlim([0.1, 100])
ax.set_ylim([0, 5])

ax.text(0.15, 0.85/1.1*5, '(b)')
ax.text(0.15, 0.2,
        r'H$_2$/Air'+'\n'
        +r'$p=10\;\mathrm{atm}$ $\phi=0.6$ $T_u=300\;\mathrm{K}$')

ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)

ax.set_xlabel(r'Ka')
ax.set_ylabel(r'$I_0$')
# %%
fig.savefig('fig_chemuq_I0_Lu2021.png', dpi=400)
# %%
