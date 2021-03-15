import numpy as np
from scipy import stats
import stmodels.data as std
import stmodels.LASTFS.st as stm

def sample_params(npts, nstd_T=0.1, nstd_C=0.15):

    # default values
    A = 0.317
    B = 0.033
    T = 5.5
    C = 1.0

    file_path = std.get_file('linear_regression_AB.npz')
    data = np.load(file_path)
    A_samples = data['A'][:npts]
    B_samples = data['B'][:npts]

    # standard devaition of T and C
    std_T = T * nstd_T
    std_C = C * nstd_C

    T_samples = np.random.normal(T, std_T, npts)
    C_samples = np.random.normal(C, std_C, npts)

    return A_samples, B_samples, T_samples, C_samples

def fwd_params(ur, lr,
               unburnt,fuel,oxidizer,chemistry,
               A_samples, B_samples, T_samples, C_samples):

    n_samples = len(T_samples)
    v_samples = np.zeros(n_samples)

    r = stm.Reactant(unburnt, fuel, oxidizer, chemistry)

    for i in range(n_samples):
        m = stm.Model(r,
                      A = A_samples[i], 
                      B = B_samples[i], 
                      T = T_samples[i], 
                      C = C_samples[i])

        v_samples[i] = m.ratio_turbulent_burning_velocity(ur, lr)

    return v_samples

def fwd_chem(ur, lr, unburnt, sc0, dl0, Le, sigma, flame_samples):

    n_samples = flame_samples[::2].shape[0]
    v_samples = np.zeros(n_samples)

    for i in range(n_samples):

        dl = flame_samples[2*i,0]
        ReF = flame_samples[2*i+1,0]
        sc = flame_samples[2*i+1,1]

        I0_table = np.zeros(flame_samples[2*i:2*i+2,1:].shape)
        I0_table[0] = flame_samples[2*i,1:] * Le
        I0_table[1] = flame_samples[2*i+1,1:] / sc

        rsc = sc0/sc
        rdl = dl0/dl

        r = stm.Reactant(unburnt, 'progvar', 
                         Le=Le, sigma=sigma, ReF=ReF, I0_table=I0_table)
        m = stm.Model(r)

        v_samples[i] = m.ratio_turbulent_burning_velocity(ur*rsc, lr*rdl)

    return v_samples

def fwd_chem_para(ur, lr, unburnt, sc0, dl0, Le, sigma, flame_samples,
                  A_samples, B_samples, T_samples, C_samples):

    n_samples = flame_samples[::2].shape[0]
    v_samples = np.zeros(n_samples)

    for i in range(n_samples):

        dl = flame_samples[2*i,0]
        ReF = flame_samples[2*i+1,0]
        sc = flame_samples[2*i+1,1]

        I0_table = np.zeros(flame_samples[2*i:2*i+2,1:].shape)
        I0_table[0] = flame_samples[2*i,1:] * Le
        I0_table[1] = flame_samples[2*i+1,1:] / sc

        rsc = sc0/sc
        rdl = dl0/dl

        r = stm.Reactant(unburnt, 'progvar', 
                         Le=Le, sigma=sigma, ReF=ReF, I0_table=I0_table)
        m = stm.Model(r,
                      A = A_samples[i], 
                      B = B_samples[i], 
                      T = T_samples[i], 
                      C = C_samples[i])

        v_samples[i] = m.ratio_turbulent_burning_velocity(ur*rsc, lr*rdl)

    return v_samples

def fwd_lr(ur, lr_samples,
           unburnt,fuel,oxidizer,chemistry):
    
    n_samples = len(lr_samples)
    v_samples = np.zeros(n_samples)

    mixture = stm.Mixture(unburnt, fuel, oxidizer, chemistry)

    for i, lr in enumerate(lr_samples):
        v_samples[i] = mixture.ratio_turbulent_burning_velocity(ur, lr)

    return v_samples

def fwd_params_lr(ur, lr_samples,
                  unburnt,fuel,oxidizer,chemistry,
                  A_samples, B_samples, T_samples, C_samples):

    n_samples = len(T_samples) * len(lr_samples)
    v_samples = np.zeros(n_samples)

    for i in range(n_samples):
        mixture = stm.Mixture(unburnt, fuel, oxidizer, chemistry,
                              A = A_samples[i], 
                              B = B_samples[i], 
                              T = T_samples[i], 
                              C = C_samples[i])

        for j, lr in enumerate(lr_samples):
            v_samples[i*len(lr_samples)+j] = mixture.ratio_turbulent_burning_velocity(ur, lr)

    return v_samples
