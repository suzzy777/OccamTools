import os
from occamtools.read_fort1 import Fort1
from occamtools.read_fort7 import Fort7
from occamtools.read_xyz import Xyz
from occamtools.occam_data import (OccamData, _check_internal_consistency_all,
                                   _check_internal_consistency)


file_name_fort_1 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'fort.1')
file_name_fort_7 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'fort.7')
file_name_fort_xyz = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                  'fort.8')


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
    ignore = ['file_name', 'n_time_steps_', 'file_contents',
              'comment_format_known']
    for f in (fort1, fort7, xyz):
        for key in f.__dict__:
            assert key in occam_data.__dict__ if key not in ignore else True


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
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(fort1.file_name, None, None)
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(None, fort7.file_name, None)
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)
    occam_data = OccamData(None, None, xyz.file_name)
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)


def test_occam_data_attributes():
    occam_data, fort1, fort7, xyz = _create_default_occam_data_object()
    _assert_all_attributes_present(occam_data, fort1, fort7, xyz)
