import os
import numpy as np
import json

def get_case(case_name):

    path = os.path.abspath(os.path.dirname(__file__))
    case_file = '{}.json'.format(case_name)
    
    case_path = os.path.join(path, case_file)

    with open(case_path, 'r') as f:
        data = json.load(f)

    return data