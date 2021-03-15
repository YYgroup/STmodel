import numpy as np
from scipy.optimize import curve_fit
import stmodels.data.cases as stc
import stmodels.LASTFS.st as stm

# fit C0 for a set of data from a case
# also calculate Ma, Le, Ze
def case_fit_C0(case_name, **kwargs):

    cases = stc.case.CaseSet(case_name)

    params = {}

    for case in cases.cases:

        case_params = {}

        case_data = cases.get_case_data(case)

        reactant = cases.get_reactant(case)

        # model prediction with given C0, as the fit function for case_fit_C0
        def case_model_predictions(case, C0):

            ur, lr = case

            model = stm.Model(reactant, C=C0, type_C0='const', Ka_def='Bradley')
            sr_model = np.zeros(len(ur))

            for i, u in enumerate(ur):
                sr_model[i] = model.ratio_turbulent_burning_velocity(u, lr[i])
            
            return sr_model

        u = case_data.turbulence_intensity
        l = case_data.turbulence_length_scale
        s = case_data.turbulent_burning_velocity

        popt, pcov = curve_fit(case_model_predictions, 
                               (u, l), s)

        case_params['np'] = len(s)
        case_params['C0'] = popt
        case_params['Le'] = reactant.Le
        case_params['Re'] = reactant.ReF
        case_params['Ze'] = reactant.flame_state.Ze()
        case_params['Er'] = reactant.flame_state.expansion()

        params[case] = case_params

    return params

# fit A and B for a set of data from a case
# also calculate Ma, Le, Ze
def case_fit_A(case_name, **kwargs):

    cases = stc.case.CaseSet(case_name)

    params = {}

    for case in cases.cases:

        case_params = {}

        case_data = cases.get_case_data(case)

        reactant = cases.get_reactant(case)

        # model prediction with given C0, as the fit function for case_fit_C0
        def case_model_predictions(case, a):

            ur, lr = case

            model = stm.Model(reactant, A=a, B=0.0)
            sr_model = np.zeros(len(ur))

            for i, u in enumerate(ur):
                sr_model[i] = model.ratio_turbulent_burning_velocity(u, lr[i])
            
            return sr_model

        u = case_data.turbulence_intensity
        l = case_data.turbulence_length_scale
        s = case_data.turbulent_burning_velocity

        popt, pcov = curve_fit(case_model_predictions, 
                               (u, l), s)

        case_params['np'] = len(s)
        case_params['A'] = popt
        case_params['Le'] = reactant.Le
        case_params['Re'] = reactant.ReF
        case_params['Ze'] = reactant.flame_state.Ze()

        params[case] = case_params

    return params