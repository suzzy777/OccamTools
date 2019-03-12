import os
import pytest
import numpy as np
from occamtools.read_xyz import Xyz

file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                         'example_fort.8')


def _read_default_file_name():
    xyz = Xyz(file_name)
    xyz.read_file()
    return xyz


def test_read_xyz_file():
    other_file = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                              'example_fort.5')
    xyz = Xyz(file_name)
    xyz.read_file()
    assert xyz.x.shape == (12, 25)

    del xyz
    xyz = Xyz(other_file)
    caught = False
    try:
        xyz.read_file()
    except ValueError:
        caught = True
    assert caught

    del xyz
    xyz = Xyz(other_file)
    xyz.read_file(file_name)
    assert xyz.y.shape == (12, 25)


def test_read_xyz_types():
    xyz = _read_default_file_name()
    assert 'Ar' in xyz.type_dict
    assert xyz.type_dict['Ar'] == 0
    assert np.squeeze(xyz.type).shape == (25,)
    assert all([(i == 0) for i in xyz.type])


def test_read_xyz_positions():
    xyz = _read_default_file_name()
    assert xyz.x[0, 6] == pytest.approx(6.7048148063, abs=1e-9)
    assert xyz.x[2, 18] == pytest.approx(7.9447518060, abs=1e-9)
    assert xyz.x[8, 15] == pytest.approx(6.5780688198, abs=1e-9)

    assert xyz.y[0, 6] == pytest.approx(1.6830535784, abs=1e-9)
    assert xyz.y[2, 18] == pytest.approx(3.9503403522, abs=1e-9)
    assert xyz.y[8, 15] == pytest.approx(4.9175769932, abs=1e-9)

    assert xyz.z[0, 6] == pytest.approx(4.4030514961, abs=1e-9)
    assert xyz.z[2, 18] == pytest.approx(1.5187645491, abs=1e-9)
    assert xyz.z[8, 15] == pytest.approx(3.3215257040, abs=1e-9)


def test_read_xyz_time_array():
    xyz = _read_default_file_name()
    assert np.squeeze(xyz.time).shape == (12,)
    assert xyz.time[0] == pytest.approx(0, abs=1e-9)
    assert xyz.time[1] == pytest.approx(0.03, abs=1e-9)
    assert xyz.time[2] == pytest.approx(0.3, abs=1e-9)
    assert xyz.time[11] == pytest.approx(3.0, abs=1e-9)
