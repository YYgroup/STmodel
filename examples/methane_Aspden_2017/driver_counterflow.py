# %%

## load packages
import pyutils.filename as fn
import pyutils.ctutils.driver as ctd
import STmodel.data.cases as stc

# %%

## get chemical kinetic model, fuel and oxidizer stream composition
cs = stc.case.CaseSet('Aspden_2017_methane')

mech = cs.get_mechanism()
fuel = cs.get_fuel_stream()
oxys = cs.get_oxy_stream()

## alternatively, user can specify these info manually as
#mech = 'hydrogen_Burke_N2.cti'
#fuel = {'H2':1.0}
#oxys = {'O2':1.0, 'N2':3.76}

# %%

## get the T, p, phi conditions in the case set
cases = cs.cases

## alternatively, user can specify these info manually as
cases = ['T-298_p-1_phi-0.7',]

# %%

## run 1D simulations for the corresponding conditions
## it will generate a folder containing flame solutions for each condition 
for condition in cases:
    
    # get unburnt status T, p, phi from condition string
    para = fn.name2params(condition)
    T = para['T']
    p = para['p']
    phi = para['phi']
    
    # calculate freely propagating flame and 
    # counterflow flames from weak stretch to extinction
    ctd.counterflow_premixed_extinction(
        chemistry=mech,             # chemical kinetic model
        fuel=fuel, oxidizer=oxys,   # fuel and oxidizer stream
        T=T, p=p, phi=phi,          # unburnt status T, p, phi
        ct_ratio=2.0, ct_slope=0.1, # numerical settings for flame solver
        ct_curve=0.1, ct_prune=0.05,# check cantera for settings
        a_init=100.,                # mean strain rate for the first point of the counterflow simulations
        a_max=2000.,                # max mean strain rate for counterflow simulation
        L_init=0.05                 # domain length for the first point of the counterflow simulations
        )

# %%
