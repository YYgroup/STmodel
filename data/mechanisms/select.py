import os
import json

def get_mech_path(mechanism):
    path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(path, mechanism)

def __get_dict():

    file_path = get_mech_path('default_mechanisms.json')

    with open(file_path, 'r') as f:
        default_mechanisms = json.load(f)

    return default_mechanisms
        
def get_fuel_name(fuel, chemistry=None):

    if chemistry is not None:
        return fuel

    default_mechanisms = __get_dict()

    name = default_mechanisms.get(fuel)[0]

    return name

def get_mechanism(fuel, chemistry=None):

    if chemistry is not None:
        return chemistry

    default_mechanisms = __get_dict()

    mech = default_mechanisms.get(fuel)[1]

    return get_mech_path(mech)

def get_fuel_mech(fuel, chemistry=None):

    fuels = get_fuel_name(fuel, chemistry)
    mech = get_mechanism(fuel, chemistry)

    return fuels, mech