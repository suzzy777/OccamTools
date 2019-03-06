import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from generate_fort5 import generate_uniform_random  # noqa: E402


def test_generate_random_uniform():
    # Test that path names given result in a file called 'fort.5' created in
    # the given path.
    path_name = os.path.join(os.path.dirname(__file__), '..')
    path_file = os.path.join(os.path.join(path_name, 'fort.5'))
    if os.path.exists(path_file):
        os.remove(path_file)
    generate_uniform_random(1, [1, 1, 1], path=path_name)
    assert os.path.exists(path_file)
    if os.path.exists(path_file):
        os.remove(path_file)

    # Test that a specific file name given results in a file of that name, at
    # the specified path is created.
    file_name = 'fort.5'
    file_name = os.path.join(os.path.dirname(__file__), file_name)
    if os.path.exists(file_name):
        os.remove(file_name)

    n_particles = 10
    box = [2, 7, 11]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        # Expected:
        # ---------------------------------------------------------------------
        # Box:
        # 2.00000    7.00000   11.00000    0.00000
        line = in_file.readline().strip()
        assert line.lower() == 'box:'
        line = in_file.readline()
        line = line.split()
        assert len(line) == 4
        for i in range(3):
            assert float(line[i]) == pytest.approx(box[i], abs=1e-15)
            assert float(line[3]) == pytest.approx(0.0, abs=1e-15)

        # Expected:
        # ---------------------------------------------------------------------
        # Number of particles:
        # 10
        line = in_file.readline().strip()
        sline = line.split()
        assert len(sline) == 3
        expected = ['Number', 'of', 'particles:']
        for i, e in enumerate(expected):
            assert sline[i] == e

        for i in range(n_particles):
            pass

        if os.path.exists(file_name):
            os.remove(file_name)


if __name__ == '__main__':
    test_generate_random_uniform()
