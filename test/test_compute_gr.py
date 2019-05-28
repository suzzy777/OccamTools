import os
import pytest
import numpy as np
from occamtools.occam_data import OccamData
from occamtools.compute_gr import compute_gr


fort1_file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                               'fort.1')
f_tmp = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                     'fort.1')

def test_compute_gr_type():
    data = OccamData(fort1_file_name, silent=True)
    compute_gr(data)

    for inp in [None, np.empty(shape=(5, 11, 3)), 1, 'not occamdata']:
        with pytest.raises(TypeError, match='type OccamData'):
            compute_gr(inp)


def test_compute_gr_simple():
    data = OccamData(fort1_file_name, silent=True)
    d0, d1, dr = 0, 2.5, 0.5
    bins_expected = np.array([0.25, 0.75, 1.25, 1.75, 2.25, 2.75]) - dr/2
    gr, bins = compute_gr(data, steps=1, bins=bins_expected,
                          range=(0, 2.5))
    gr_expected = [0.0, 0.45472840883398674, 1.1727206333087026,
                   0.8602969896859208, 1.0436389710943959, 0.9463266886545127]
    bins_expected = np.array([0.25, 0.75, 1.25, 1.75, 2.25, 2.75]) - dr/2

    gr_expected = list(gr_expected)
    gr = list(gr)
    for _ in range(5):
        gr_expected.append(None)
        gr.append(None)

    print("")
    for be, bb in zip(bins_expected, bins):
        print(f"{be if be is not None else -1:<20f}"
              f"{bb if bb is not None else -1:<20f}"
              f"{abs(be - bb) if (be is not None and bb is not None) else -1:<20f}")
    print("")
    for ge, gg in zip(gr_expected, gr):
        print(ge, gg)
        print(f"{ge:<20f} {gg:<20f} {abs(ge - gg):<20f}")


if __name__ == '__main__':
    test_compute_gr_simple()
