import numpy as np
from occamtools.occam_data import OccamData


def histogram(data, dimension=None, time_steps=None):
    if isinstance(data, OccamData):
        d = data.x
    elif isinstance(data, np.ndarray):
        d = data
    else:
        error_str = (f'Given data must be of type OccamData or np.ndarray, not'
                     f' {type(data)}.')
        raise TypeError(error_str)

    return np.zeros(2)
