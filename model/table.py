import os
import glob
import numpy as np
import pyutils.filename as fn
import pyutils.fig as fg
import pyutils.ctutils.flame as ctf
import pyutils.ctutils.mechanisms.select as ms

class OneDimTable():
    
    def __init__(self, table):

        self.x = table[0]
        self.y = table[1]

    def retrieve(self, x):

        return np.interp(x, self.x, self.y)

    def print(self, filename):

        data = np.zeros((self.x.size, 2))

        data[:,0] = self.x
        data[:,1] = self.y

        np.savetxt(filename, data, fmt='%20.10E', delimiter='')

        return 0


class FlameStretchTable(OneDimTable):
    
    def __init__(self, 
                 unburnt, 
                 fuel, 
                 oxidizer={'O2':1., 'N2':3.76}, 
                 chemistry=None, 
                 Ka_min=0.01):

        table_name='stretch_factor_table.npy'
        table_file = '{0}/{1}'.format(unburnt, table_name)
        
        #try:
        if os.path.isfile(table_file):

            data = np.load(table_file)

        #except FileNotFoundError:
        else:

            fuels, mech = ms.get_fuel_mech(fuel, chemistry)

            # load the free flame
            solution = '{0}/{0}.xml'.format(unburnt)

            # get flame state
            fs_0 = ctf.FreeFlameState(solution, mech, fuels, oxidizer)

            array_0 = np.array((0., 1.))

            sc = fs_0.consumption_speed()
            df = fs_0.thermal_thickness()

            # get strain rate list

            flame_params = fn.name2params(unburnt)
            flame_params['a'] = '*'
            flame_name = fn.params2name(flame_params)

            flame_list = glob.glob('{}/{}.xml'.format(unburnt, flame_name))
            a_list = np.empty(len(flame_list))

            for i, f in enumerate(flame_list):
                params = fn.name2params(f[len(unburnt)+2:-4])
                a_list[i] = params['a']

            a_list = np.sort(a_list)

            # get stretched flame

            array_a = np.zeros((2, a_list.size))

            for i, a in enumerate(a_list):

                flame_params['a'] = a
                flame_name = fn.params2name(flame_params)

                solution = '{}/{}.xml'.format(unburnt, flame_name)

                fs_a = ctf.CounterflowPremixedFlameState(solution, mech, fuels, oxidizer, fs_0.T_peak())
                #fs_a = ctf.CounterflowPremixedFlameState(solution, mech, fuels, oxidizer)
            
                array_a[0,i] = fs_a.strain_rate() * df / sc
                array_a[1,i] = fs_a.consumption_speed() / sc

            # remove the point with small Ka
            flag = array_a[0] > Ka_min

            data = np.column_stack((array_0, array_a[:,flag]))

            np.save(table_file, data)

        OneDimTable.__init__(self, data)

    def Ma(self, npts=6):

        Ka = self.x
        I0 = self.y

        p = np.polyfit(Ka[:npts], I0[:npts], deg=1)

        return -p[0]

    def plot_stretch_factor(self, fig_name, xlim=[0.1, 50.], ylim=[0., 2.]):

        config = fg.PlotConfig(config_name="slides_single")
        fig, ax = config.get_simple()

        ax.plot(self.x, self.y, 'ok')
        ax.plot(self.x, self.y, '--r')

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        ax.set_xscale('log')

        ax.set_xlabel(r'$\mathrm{Ka}$')
        ax.set_ylabel(r'$I_0$')

        fig.savefig(fig_name, dpi=400)

        fg.close(fig)

        return

    def plot_Markstein_fit(self, fig_name, npts=5, xlim=[0., 1.], ylim=[0., 2.]):
        
        config = fg.PlotConfig(config_name="slides_single")
        fig, ax = config.get_simple()

        ax.plot(self.x, self.y, 'ok')

        x = np.linspace(0, 1)
        y = 1 - self.Ma(npts)*x

        ax.plot(x, y, '--r')

        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        ax.set_xlabel(r'$\mathrm{Ka}$')
        ax.set_ylabel(r'$I_0$')

        fig.savefig(fig_name, dpi=400)

        fg.close(fig)

        return
