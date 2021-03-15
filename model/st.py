import numpy as np
import scipy.special as sp
import pyutils.filename as fn
import pyutils.ctutils.flame as ctf
import stmodels.LASTFS.table as stt
import pyutils.ctutils.mechanisms.select as ms

class Model():
    
    def __init__(self, reactant, A=0.3168, B=0.03315, T=5.5, C=1.0, **kwargs):

        self.reactant = reactant

        self.A = A
        self.B = B
        self.T = T
        self.C = C

        # parameters
        if 'Ka_def' in kwargs.keys():
            self.Ka_def = kwargs['Ka_def']
        else:
            self.Ka_def = 'Bradley'

        if 'type_C0' in kwargs.keys():
            self.type_C0 = kwargs['type_C0']
        else:
            self.type_C0 = 'instability'

        if 'C_lr' in kwargs.keys():
            self.C_lr = kwargs['C_lr']
        else:
            self.C_lr = 0.5

    def ratio_turbulent_burning_velocity(self, ur, lr):


        I0 = self.stretch_factor(ur, lr)

        Ar = self.ratio_flame_surface(ur, lr)

        sr = I0 * Ar

        return sr

    def ratio_flame_surface(self, ur, lr):

        sc = self.reactant.laminar_flame_speed

        I0 = self.stretch_factor(ur, lr)

        xi = self.T * (self.A+self.B*sc*np.square(I0))

        growth_rate = xi + self.C_lr * np.log(lr)

        #I0_p = self.stretch_factor(1.0, 1.0)
        I0_p = self.reactant.stretch_factor_table.retrieve(1.0/self.reactant.Le)

        C = I0_p * self.C0()

        #Re = self.Re(ur, lr)
        #truncation_time = 1. - np.exp( - C
        #                               *np.power(lr, 0.5)
        #                               *np.power(Re, -0.25)/xi
        #                               *ur/I0)

        # avoid singular point at u'=0
        ReF = self.reactant.ReF
        truncation_time = 1. - np.exp( - C
                                      *np.power(lr, self.C_lr-0.25)
                                      *np.power(ReF, -0.25)/xi
                                      *np.power(ur, 1.0-0.25)/I0)

        return np.exp(growth_rate*truncation_time)

    def turbulent_burning_velocity(self, ur, lr):

        sc = self.reactant.laminar_flame_speed
        sr = self.ratio_turbulent_burning_velocity(ur, lr)
        st = sr * sc

        return st

    def Re(self, ur, lr):
        return ur * lr * self.reactant.ReF

    def Ka(self, ur, lr):

        def Ka_Bradley(ur, lr):
            return 0.157 * np.power(ur, 1.5) / np.power(lr, 0.5) / np.power(self.reactant.ReF, 0.5)

        def Ka_Lu(ur, lr):
            return 0.1 * ur / lr

        switch = {'Bradley':Ka_Bradley,
                  'Lu':Ka_Lu}

        K = switch.get(self.Ka_def)(ur, lr)
        
        f = np.power(self.reactant.p, 0.5) / self.reactant.Le

        return f * K

    def stretch_factor(self, ur, lr):
        Ka = self.Ka(ur, lr)
        I0 = self.reactant.stretch_factor_table.retrieve(Ka)
        return I0

    def C0(self):

        def C0_const():
            return self.C

        def C0_Le():
            return self.C / self.reactant.Le

        def C0_instability():
            return self.C * (1.0-self.reactant.sigma) / self.reactant.Le

        switch = {'const':C0_const,
                  'Le':C0_Le,
                  'instability':C0_instability}

        return switch.get(self.type_C0)()

class Reactant():

     def __init__(self, 
                 unburnt, 
                 fuel, 
                 oxidizer={'O2':1., 'N2':3.76}, 
                 chemistry=None, 
                 **kwargs):

        if 'type_Le' in kwargs.keys():
            self.type_Le = kwargs['type_Le']
        else:
            self.type_Le = 'unburnt'

        if 'laminar_flame_speed' in kwargs.keys():
            sc = kwargs['laminar_flame_speed']
        else:
            sc = 1.0

        if 'Le' in kwargs.keys():
            Le = kwargs['Le']
        else:
            Le = 1.0

        if 'sigma' in kwargs.keys():
            sigma = kwargs['sigma']
        else:
            sigma = 1.0/6.0

        if 'Re_flame' in kwargs.keys():
            ReF = kwargs['Re_flame']
        else:
            ReF = 10.0

        if 'I0_table' in kwargs.keys():
            I0_table = kwargs['I0_table']
        else:
            I0_table = np.array([[0.0, 10.0],[1.0, 1.0]])

        ##################################################

        # get pressure and equivalence ratio

        params = fn.name2params(unburnt)

        self.p = params['p']

        if fuel is 'progvar':

            self.Le = Le

            self.sigma = sigma

            self.ReF = ReF

            self.laminar_flame_speed = sc

            self.stretch_factor_table = stt.OneDimTable(I0_table)

        else:

            # get state of the unstretched flame

            file_name = '{0}/laminar_info.npz'.format(unburnt)

            fuels, mech = ms.get_fuel_mech(fuel, chemistry)

            try:

                data = np.load(file_name)

                self.Le = data['Le']
                self.sigma = data['sigma']
                self.ReF = data['ReF']
                self.laminar_flame_speed = data['sc']

            except FileNotFoundError:

                solution = '{0}/{0}.xml'.format(unburnt)

                self.flame_state = ctf.FreeFlameState(solution, mech, fuels, oxidizer)

                self.Le = self.flame_state.Le_eff(self.type_Le)

                self.sigma = self.flame_state.expansion()

                self.ReF = self.flame_state.Re()

                self.laminar_flame_speed = self.flame_state.consumption_speed()

                np.savez(file_name,
                         Le=self.Le,
                         sigma=self.sigma,
                         ReF=self.ReF,
                         sc=self.laminar_flame_speed)

            # get stretch factor table

            self.stretch_factor_table = stt.FlameStretchTable(
                unburnt, fuels, oxidizer, mech) 
