import os
from . import cases

def get_file(file):
    path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(path, file)
