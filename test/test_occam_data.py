import os
from occamtools.read_fort1 import Fort1
from occamtools.read_fort7 import Fort7
from occamtools.read_xyz import Xyz
from occamtools.occam_data import (_check_internal_consistency_all,
                                   _check_internal_consistency)


file_name_fort_1 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'example_3_fort.1')
file_name_fort_7 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                'example_fort.7')
file_name_fort_xyz = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                                  'example_fort.8')


def _load_default_forts():
    fort1 = Fort1(file_name_fort_1)
    fort1.read_file()
    fort7 = Fort7(file_name_fort_7)
    fort7.read_file()
    xyz = Xyz(file_name_fort_xyz)
    xyz.read_file()
    return fort1, fort7, xyz


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
