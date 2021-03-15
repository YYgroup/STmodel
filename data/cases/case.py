import os
import numpy as np
import json
import pyutils.filename as fn
from scipy.optimize import curve_fit
import pyutils.ctutils.mechanisms.select as ms
import stmodels.LASTFS.st as stm

class DataSet():

    def __init__(self, data):

        len_data = len(data)

        ur = np.zeros(len_data)
        lr = np.zeros(len_data)
        sr = np.zeros(len_data)
        sr_std = np.zeros(len_data)

        for i in range(len_data):
            ur[i] = data[i].get('ur')
            lr[i] = data[i].get('lr')
            sr[i] = data[i].get('sr')
            sr_std[i] = data[i].get('sr_std', 0.0)

        self.turbulence_intensity = ur
        self.turbulence_length_scale = lr
        self.turbulent_burning_velocity = sr
        self.turbulent_burning_velocity_std = sr_std

class CaseSet():
    
    def __init__(self, case_name):

        self.case_name = case_name

        data_json = self.__get_data(case_name)

        self.fuel = data_json.get('fuel')
        self.oxidizer = data_json.get('oxidizer', {'O2':1., 'N2':3.76})
        self.mechanism = ms.get_mechanism(self.fuel, data_json.get('mechanism'))

        self.reference = data_json.get('reference')
        self.configuration = data_json.get('configuration')

        self.cases = list(data_json.get('cases').keys())

        data = {}
        for case in self.cases:
            data[case] = DataSet(data_json.get('cases').get(case))

        self.data = data

    def __get_data(self, filename):

        path = os.path.abspath(os.path.dirname(__file__))
        file_name = fn.add_suffix(filename, 'json')
        file_path = os.path.join(path, file_name)

        with open(file_path, 'r') as f:
            data = json.load(f)

        return data
        
    def get_fuel_stream(self):
        return ms.get_fuel_name(self.fuel)

    def get_oxy_stream(self):
        return self.oxidizer

    def get_mechanism(self):
        return ms.get_mech_path(self.mechanism)

    def get_case_data(self, unburnt):
        return self.data.get(unburnt)

    def get_reactant(self, unburnt, **kwargs):
        return stm.Reactant(unburnt, 
                            self.get_fuel_stream(),
                            self.get_oxy_stream(),
                            self.get_mechanism(),
                            **kwargs)

    # marker in diagram, dependent on fuel
    def get_marker(self):
        dict_marker = self.__get_data('config_plot').get('dict_fuel_marker')
        marker = dict_marker.get(self.fuel)
        return marker

    # color dependent on pressure
    def get_case_color(self, unburnt):
        dict_color = self.__get_data('config_plot').get('dict_p_color')
        p = fn.name2params(unburnt).get('p')
        p_str = '{:g}'.format(np.around(p))
        color = dict_color.get(p_str)
        return color
