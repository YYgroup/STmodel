# %%
import numpy as np
from scipy import stats
import pyutils.fig as fg
# %%
d = np.load('free_flame.npz')
sl = d['sl']
dl = d['dl']
# %%
pdf, xedges, yedges = np.histogram2d(dl, sl, bins=200, 
                                     density=True)

xidx = np.clip(np.digitize(dl, xedges)-1, 0, pdf.shape[0]-1)
yidx = np.clip(np.digitize(sl, yedges)-1, 0, pdf.shape[1]-1)
c = pdf[xidx, yidx]
# %%
kde_sl = stats.gaussian_kde(sl)
x_sl = np.linspace(0,1.1,num=200)
pdf_sl = kde_sl(x_sl)
# %%
kde_dl = stats.gaussian_kde(dl*1e6)
x_dl = np.logspace(1,3,num=200)
pdf_dl = kde_dl(x_dl)
# %%
pc = fg.PlotConfig('manuscript_single')
# %%
fig, ax = pc.get_simple()

color_plot=ax.scatter(dl*1e6,sl,c=c,s=4,vmin=0,vmax=1e6)

ax.set_xscale('log')
ax.set_xlim([10,1000])
ax.set_ylim([0,1.1])
ax.set_xticks(np.logspace(1,3,num=3))

ax.set_xlabel(r'$\delta_L^0\;\mathrm{(\mu m)}$')
ax.set_ylabel(r'$s_L^0\;\mathrm{(m/s)}$')

ax.tick_params(which='major', direction='in', bottom=True, top=True, left=True, right=True)

#ax.text(420, 0.49, r'CH$_4$/Air'+'\n'+r'$p=1\;\mathrm{atm}$ $\phi=0.89$ $T_u=298\;\mathrm{K}$')
ax.text(100, 0.9, r'$s_L^0\;\mathrm{m/s}$')
ax.text(100, 0.8, r'$\delta_L^0\;\mathrm{\mu m}$')
ax.text(300, 1.0, r'$\mu$')
ax.text(600, 1.0, r'$\sigma$')
ax.text(300, 0.9, '{:.2f}'.format(np.average(sl)))
ax.text(300, 0.8, '{:.1f}'.format(np.average(dl)*1e6))
ax.text(600, 0.9, '{:.2f}'.format(np.std(sl)))
ax.text(600, 0.8, '{:.1f}'.format(np.std(dl)*1e6))

cax = fig.add_axes([0.7, 0.6, 0.2, 0.02])
cbar = fig.colorbar(color_plot, 
                    cax=cax, 
                    ticks=[0,5e5,10e5],
                    orientation='horizontal')
cbar.ax.set_xticklabels([0, 5, 10])
cax.tick_params(direction='in')
cax.set_title(r'PDF $\times10^5$')

ax_pdf = fig.add_axes([pc.margin_left/pc.plot_width, 
                      pc.margin_bottom/pc.plot_height,
                      pc.subplot_width/pc.plot_width,
                      pc.subplot_height/pc.plot_height
                      ],
                     fc='none', frameon=False)

ax_pdf.plot(pdf_sl*4+10, x_sl, 'r')
ax_pdf.plot(x_dl, pdf_dl*6, 'b')

ax_pdf.set_xscale('log')
ax_pdf.set_xlim([10, 1000])
ax_pdf.set_ylim([0, 1.1])

ax_pdf.set_xticks([])
ax_pdf.set_yticks([])

# %%
fig.savefig('fig_chemuq_sc_dl_Lu2021.png', dpi=200)
# %%
