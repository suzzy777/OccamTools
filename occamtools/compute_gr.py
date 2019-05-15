import numpy as np
from occamtools import OccamData


def compute_gr(data):
    if not isinstance(data, OccamData):
        error_str = (f'Given data must be of type OccamData, not {type(data)}')
        raise TypeError(error_str)
