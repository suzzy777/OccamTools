import os
import numpy as np
import pytest
from occamtools.occam_data import OccamData
from occamtools.histogram import histogram as occamhist
from occamtools.histogram import _check_time_steps

fort1_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                             'data', 'fort.1'))


def test_histogram_input_type():
    occamdata = OccamData(fort1_file, silent=True)
    npdata = occamdata.x
    for d in (occamdata, npdata):
        hist, _ = occamhist(d)
        assert isinstance(hist, np.ndarray)

    for d in (1, 'not', 2.45):
        caught = False
        try:
            occamhist(d)
        except TypeError:
            caught = True
        assert caught is True


def test_histogram_dimension(capsys):
    data = OccamData(fort1_file, silent=True)
    for dim in (0, 1, 2, 'x', 'y', 'z', None):
        hist, _ = occamhist(data, dimension=dim)
        assert isinstance(hist, np.ndarray)

    for dim in (-1, 3, 4):
        caught = False
        try:
            occamhist(data, dimension=dim)
        except ValueError:
            caught = True
        assert caught is True

    for dim in ('a', 'not', 'here be dragons'):
        caught = False
        try:
            occamhist(data, dimension=dim)
        except TypeError:
            caught = True
        assert caught is True

    with pytest.warns(UserWarning, match='dimension keyword'):
        occamhist(data.x, dimension=1)


def test_histogram_time_steps():
    data = OccamData(fort1_file, silent=True)
    d = data.x

    for time_step in ((0, -1), [0, -1], np.array([0, -1]), (-len(d), -1)):
        ts = _check_time_steps(d, time_step)
        assert ts[0] == 0
        assert ts[1] == len(d)-1

    for time_steps in ('here be dragons', (1, 200)):
        caught = False
        try:
            _check_time_steps(d, time_steps)
        except ValueError:
            caught = True
        assert caught is True
