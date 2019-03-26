import os
import pytest
from occamtools.replace_in_fort1 import replace_in_fort1
from occamtools.read_fort1 import Fort1
from test.test_occam_data import _check_equal


file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                         'fort.1')
fort1 = Fort1(file_name)
fort1.read_file()


def _assert_fort1s_equal_ignore(a, b, *args):
    ignore = ['file_name', 'file_contents', 'title']
    for arg in args:
        assert isinstance(arg, str)
        ignore.append(arg)
    for key in a.__dict__:
        assert key in b.__dict__
        if key not in ignore:
            assert _check_equal(a.__dict__[key], b.__dict__[key])


def test_replace_in_fort1_file():
    out_file_name = replace_in_fort1(file_name, None)
    assert os.path.basename(out_file_name) == 'fort.1_new'
    assert os.path.exists(out_file_name) and os.path.isfile(out_file_name)
    os.remove(out_file_name)

    out_file_name = 'fort.1_replace'
    replace_in_fort1(file_name, out_file_name)
    assert os.path.exists(out_file_name) and os.path.isfile(out_file_name)
    os.remove(out_file_name)


def test_replace_in_fort1_int():
    out_file_name = os.path.join(os.path.dirname(file_name), 'fort.1_int')
    for steps, atoms in zip([54144, 901, 129, 598], [90, 1598, 2515, 1001]):
        replace_in_fort1(file_name, out_file_name,
                         atoms=atoms, number_of_steps=steps)
        fort1_new = Fort1(out_file_name)
        fort1_new.read_file(silent=True)
        assert fort1_new.n_particles == atoms
        assert fort1_new.n_time_steps == steps
        _assert_fort1s_equal_ignore(fort1, fort1_new,
                                    'n_particles', 'n_time_steps')
    os.remove(out_file_name)


def test_replace_in_fort1_float():
    out_file_name = os.path.join(os.path.dirname(file_name), 'fort.1_float')

    for dt, freq in zip([0.1, 0.02, 1.085, 0.295], [1.0, 6.294, 0.0258, 9]):
        replace_in_fort1(file_name, out_file_name,
                         time_step=dt, collision_frequen=freq)
        fort1_new = Fort1(out_file_name)
        fort1_new.read_file(silent=True)
        assert fort1_new.dt == pytest.approx(dt, abs=1e-14)
        assert fort1_new.collision_frequency == pytest.approx(freq, abs=1e-14)
        _assert_fort1s_equal_ignore(fort1, fort1_new,
                                    'dt', 'collision_frequency')
    os.remove(out_file_name)
