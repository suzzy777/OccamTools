import os
import numpy as np
import warnings
from occamtools.read_xyz import _are_floats, Xyz
from occamtools.read_fort1 import Fort1
from occamtools.read_fort7 import Fort7


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


def _open_fort_files(fort1, fort7, xyz, which=None):
    if which is None:
        f1 = Fort1(fort1)
        f7 = Fort7(fort7)
        x = Xyz(xyz)
    else:
        if which == 0:
            f1 = fort1
            f7 = os.path.join(os.path.dirname(fort1), 'fort.7')
            x = os.path.join(os.path.dirname(fort1), 'fort.8')
        elif which == 1:
            f1 = os.path.join(os.path.dirname(fort7), 'fort.1')
            f7 = fort7
            x = os.path.join(os.path.dirname(fort7), 'fort.8')
        elif which == 2:
            f1 = os.path.join(os.path.dirname(xyz), 'fort.1')
            f7 = os.path.join(os.path.dirname(xyz), 'fort.7')
            x = xyz
        f1 = Fort1(f1)
        f7 = Fort7(f7)
        x = Xyz(x)

    for f in (f1, f7, x):
        f.read_file()
    return f1, f7, x


def _check_constructor_input(fort1, fort7, xyz):
    if (isinstance(fort1, Fort1) and isinstance(fort7, Fort7)
            and isinstance(xyz, Xyz)):
        return fort1, fort7, xyz
    elif (isinstance(fort1, str) and isinstance(fort7, str)
            and isinstance(xyz, str)):
        return _open_fort_files(fort1, fort7, xyz)
    elif isinstance(fort1, str):
        return _open_fort_files(fort1, fort7, xyz, which=0)
    elif isinstance(fort7, str):
        return _open_fort_files(fort1, fort7, xyz, which=1)
    elif isinstance(xyz, str):
        return _open_fort_files(fort1, fort7, xyz, which=2)
    else:
        raise ValueError('OccamData constructor input not recognized as Fort1/'
                         'Fort7/Xzy objects or (one or more) file paths.')


class OccamData:
    def __init__(self, fort1, fort7, xyz):
        fort1, fort7, xyz = _check_constructor_input(fort1, fort7, xyz)
        self.consistent = _check_internal_consistency_all(fort1, fort7, xyz)
        ignore = ['file_name', 'n_time_steps_', 'file_contents',
                  'comment_format_known']
        for f in (fort1, fort7, xyz):
            for key in f.__dict__:
                if key not in ignore:
                    setattr(self, key, f.__dict__[key])
        self.fort1_file_contents = fort1.file_contents
