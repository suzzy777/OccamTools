import os
import pytest
from occamtools.replace_in_fort1 import replace_in_fort1
from occamtools.read_fort1 import Fort1


file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                         'fort.1')


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
        fort1 = Fort1(out_file_name)
        fort1.read_file(silent=True)
        assert fort1.n_particles == atoms
        assert fort1.n_time_steps == steps
    os.remove(out_file_name)


def test_replace_in_fort1_float():
    out_file_name = os.path.join(os.path.dirname(file_name), 'fort.1_float')
    for dt, freq in zip([0.1, 0.02, 1.085, 0.295], [1.0, 6.294, 0.0258, 9]):
        replace_in_fort1(file_name, out_file_name,
                         time_step=dt, collision_frequen=freq)
        fort1 = Fort1(out_file_name)
        fort1.read_file(silent=True)
        assert fort1.dt == pytest.approx(dt, abs=1e-14)
        assert fort1.collision_frequency == pytest.approx(freq, abs=1e-14)
    os.remove(out_file_name)
