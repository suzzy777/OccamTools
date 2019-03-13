import numpy as np
import warnings
from occamtools.read_xyz import _are_floats


def _check_internal_consistency(a, b):
    ignore = ['file_name']
    a_vars, b_vars = a.__dict__, b.__dict__
    consistent = True
    for k in a_vars:
        if (k in b_vars) and (k not in ignore):
            warn = False
            a_val = a_vars[k]
            b_val = b_vars[k]
            if _are_floats(a_val, b_val):  # These attributes are numbers
                if not np.allclose(a_val, b_val):
                    warn = True
            elif isinstance(a_val, str) and isinstance(b_val, str):
                if not (a_val == b_val):
                    warn = True
            if warn:
                class_a, class_b = type(a).__name__, type(b).__name__
                warn_str = ('\nData is not internally consistent\n\n'
                            + '->' + str(class_a) + ' from file ' + a.file_name
                            + ': ' + str(a_val) + '\n\n'
                            + '->' + str(class_b) + ' from file ' + b.file_name
                            + ': ' + str(b_val))
                warnings.warn(warn_str)
                consistent = False
    return consistent


def _check_internal_consistency_all(fort1, fort7, xyz):
    consistent_1_7 = _check_internal_consistency(fort1, fort7)
    consistent_1_xyz = _check_internal_consistency(fort1, xyz)
    consistent_7_xyz = _check_internal_consistency(fort7, xyz)
    if consistent_1_7 and consistent_1_xyz and consistent_7_xyz:
        return True
    else:
        return False


class OccamData:
    def __init__(self, fort1, fort7, xyz):
        self.consistent = _check_internal_consistency_all(fort1, fort7, xyz)
