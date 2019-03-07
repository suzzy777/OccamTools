import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from generate_fort5 import generate_uniform_random  # noqa: E402


def check_remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        return True
    else:
        return False


def test_generate_random_uniform_path():
    # Test that path names given result in a file called 'fort.5' created in
    # the given path.
    path = os.path.join(os.path.dirname(__file__), '..')
    path_file = os.path.join(os.path.join(path, 'fort.5'))
    check_remove_file(path_file)

    generate_uniform_random(1, [1, 1, 1], path=path)
    assert check_remove_file(path_file)


def test_generate_random_uniform_file():
    # Test that a specific file name given results in a file of that name, at
    # the specified path is created.
    file_name = 'fort.5'
    file_name = os.path.join(os.path.dirname(__file__), file_name)
    check_remove_file(file_name)

    generate_uniform_random(2, [2, 3, 4], path=file_name)
    assert check_remove_file(file_name)


def test_generate_random_uniform_header():
    file_name = os.path.join(os.path.dirname(__file__), 'header_test.5')
    check_remove_file(file_name)

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

    assert check_remove_file(file_name)


def test_generate_random_uniform_n_molecules():
    file_name = os.path.join(os.path.dirname(__file__), 'molecules_test.5')
    check_remove_file(file_name)

    n_particles = 10
    box = [2, 2, 2]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(2):
            line = in_file.readline()

        # Expected:
        # ---------------------------------------------------------------------
        # Number of particles:
        # 10
        line = in_file.readline().strip()
        line = line.split()
        assert len(line) == 3
        expected = ['Number', 'of', 'particles:']
        for i, e in enumerate(expected):
            assert line[i] == e
        line = in_file.readline().strip()
        assert int(line) == n_particles


def test_generate_random_uniform_positions():
    file_name = os.path.join(os.path.dirname(__file__), 'pos_test.5')
    check_remove_file(file_name)

    n_particles = 100
    box = [9.29580019,
           6.12879582,
           3.98020502]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(4):
            line = in_file.readline()

        for i in range(1, n_particles+1):
            # Expected:
            # -----------------------------------------------------------------
            # Molecule # 1
            # 1
            # 1 Ar 1 0 0.642649076 3.78051288 3.6288812 0 0 0 0 0 0
            line = in_file.readline()
            line = line.split()
            assert int(line[-1]) == i

            line = in_file.readline().strip()
            assert int(line) == 1

            line = in_file.readline()
            line = line.split()
            assert len(line) == 13
            x, y, z = [float(p) for p in line[4:7]]
            assert x <= box[0]
            assert y <= box[1]
            assert z <= box[2]

    check_remove_file(file_name)


if __name__ == '__main__':
    test_generate_random_uniform_path()
    test_generate_random_uniform_file()
    test_generate_random_uniform_header()
    test_generate_random_uniform_n_molecules()
    test_generate_random_uniform_positions()
