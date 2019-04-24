import os
import numpy as np
from occamtools.occam_data import OccamData
from occamtools.histogram import histogram as occamhist

fort1_file = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,
                             'data', 'fort.1'))


def test_histogram_input_type():
    occamdata = OccamData(fort1_file, silent=True)
    npdata = occamdata.x
    for d in (occamdata, npdata):
        hist = occamhist(d)
        assert isinstance(hist, np.ndarray)

    for d in (1, 'not', 2.45):
        caught = False
        try:
            hist = occamhist(d)
        except TypeError:
            caught = True
        assert caught is True
