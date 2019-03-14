import os
import pytest
import numpy as np
import warnings
from occamtools.read_fort1 import Fort1
from occamtools.read_fort7 import Fort7
from occamtools.read_xyz import Xyz, _are_floats
from occamtools.occam_data import (OccamData, _check_internal_consistency_all,
                                   _check_internal_consistency)


file_name_fort_1 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'fort.1')
file_name_fort_7 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'fort.7')
file_name_fort_xyz = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                  'fort.8')
ignore = ['file_name', 'n_time_steps_', 'file_contents',
          'comment_format_known']


def _load_default_forts():
    fort1 = Fort1(file_name_fort_1)
    fort1.read_file()
    fort7 = Fort7(file_name_fort_7)
    fort7.read_file()
    xyz = Xyz(file_name_fort_xyz)
    xyz.read_file()
    return fort1, fort7, xyz


def _create_default_occam_data_object():
    fort1, fort7, xyz = _load_default_forts()
    occam_data = OccamData(fort1, fort7, xyz)
    return occam_data, fort1, fort7, xyz


def _assert_all_attributes_present(occam_data, fort1, fort7, xyz):
    for f in (fort1, fort7, xyz):
        for key in f.__dict__:
            assert key in occam_data.__dict__ if key not in ignore else True


def _check_equal(a, b):
    if _are_floats(a, b):
        return a == pytest.approx(b, abs=1e-14)
    elif isinstance(a, str) and isinstance(b, str):
        return a == b
    elif hasattr(a, 'shape') and hasattr(b, 'shape'):
        return np.allclose(a, b)
    else:
        return a == b


def _assert_all_attributes_equal(occam_data, fort1, fort7, xyz):
    for f in (fort1, fort7, xyz):
        for key in f.__dict__:
            if key not in ignore:
                assert _check_equal(f.__dict__[key], occam_data.__dict__[key])


def _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz):
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)
    _assert_all_attributes_equal(occam_data, fort1, fort7, xyz)


def test_occam_data_check_internal_consistency_1_7():
    fort1, fort7, xyz = _load_default_forts()

    c17 = _check_internal_consistency(fort1, fort7)
    assert c17
    c1x = _check_internal_consistency(fort1, xyz)
    assert c1x
    c7x = _check_internal_consistency(fort7, xyz)
    assert c7x

    all_ = _check_internal_consistency_all(fort1, fort7, xyz)
    assert all_
    assert (c17 and c1x and c7x) is all_


def test_occam_data_constructor_files():
    fort1, fort7, xyz = _load_default_forts()
    occam_data = OccamData(fort1.file_name, fort7.file_name, xyz.file_name)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(fort1.file_name, None, None)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(None, fort7.file_name, None)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(None, None, xyz.file_name)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)


def test_occam_data_attributes():
    occam_data, fort1, fort7, xyz = _create_default_occam_data_object()
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)


def test_occam_data_wrong_input():
    caught = False
    try:
        _ = OccamData(None, None, None)
    except ValueError:
        caught = True
    assert caught


def test_occam_data_not_equal():
    for i in range(2):
        fort1, fort7, xyz = _load_default_forts()
        if i == 0:
            fort1.n_particles += 1
        else:
            fort1.title = 'changed'

        warnings.filterwarnings('ignore')
        fort1.n_particles += 1
        occam_data = OccamData(fort1, fort7, xyz)
        assert occam_data.consistent is False

        warnings.filterwarnings('error')
        caught = False
        try:
            _ = OccamData(fort1, fort7, xyz)
        except Warning:
            caught = True
        assert caught
    warnings.filterwarnings('always')


def test_occam_data_single_input():
    fort1, fort7, xyz = _load_default_forts()
    occam_data = OccamData(fort1.file_name)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(fort7.file_name)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(xyz.file_name)
    _assert_all_attributes_present_and_equal(occam_data, fort1, fort7, xyz)

    inputs = ['this_is_not_a_file', None, 1, 8.29898, fort1, fort7, xyz]
    for inp in inputs:
        caught = False
        try:
            _ = OccamData(inp)
        except TypeError:
            caught = True
        except FileNotFoundError:
            caught = True
        assert caught
