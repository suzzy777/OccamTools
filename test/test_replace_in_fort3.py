import os
import pytest
import numpy as np
from occamtools.replace_in_fort3 import (Fort3Replacement,
                                         _Properties, _is_int,
                                         _count_property_instances,
                                         _count_existing_instances,
                                         _parse_fort_3_file,
                                         _sort_new_replace_args)


file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                         'example_fort.3')


def test_replace_in_fort3_fort3_parse_property_name():
    properties = ['atom', 'bond type', 'bond angle', 'torsion', 'non bonded',
                  'scf', 'compress', 'chi']
    replacement = Fort3Replacement()
    assert replacement.property is None

    for index, prop in enumerate(properties):
        replacement = Fort3Replacement(property=prop)
        assert replacement.property == index

    for s in ['abc', 'this-is-not-valid', 'a t o m', 'mota', 'not']:
        caught = False
        try:
            replacement = Fort3Replacement(property=s)
        except ValueError:
            caught = True
        assert caught is True


def test_replace_in_fort3_properties_replace_new():
    replacement = Fort3Replacement(new=True)
    assert replacement.new is True
    assert replacement.replace is False

    replacement.replace = True
    assert replacement.new is False
    assert replacement.replace is True

    replacement.new = True
    assert replacement.new is True
    assert replacement.replace is False

    for inp in ['string', 1, 8.251, int]:
        caught = False
        try:
            replacement.new = inp
        except TypeError:
            caught = True
        assert caught is True

        caught = False
        try:
            replacement.replace = inp
        except TypeError:
            caught = True
        assert caught is True

        caught = False
        try:
            replacement = Fort3Replacement(new=inp)
        except TypeError:
            caught = True
        assert caught is True

    for a, b in zip([True, False], [False, True]):
        replacement = Fort3Replacement(new=a, replace=b)
        assert replacement.new is a
        assert replacement.replace is b

    for inp in [True, False]:
        caught = False
        try:
            replacement = Fort3Replacement(new=inp, replace=inp)
        except ValueError:
            caught = True
        assert caught is True

    replacement = Fort3Replacement(new=True, replace=None)
    assert replacement.new is True
    assert replacement.replace is False

    replacement = Fort3Replacement(new=None, replace=False)
    assert replacement.new is True
    assert replacement.replace is False


def test_replace_in_fort3_fort3_properties_index():
    properties = ['atom', 'bond type', 'bond angle', 'torsion', 'non bonded',
                  'scf', 'compress', 'chi']

    for prop in properties:
        replace = Fort3Replacement(property=prop)
        expected = _Properties._type_from_index(replace.property).lower()
        if len(prop.split()) > 1:
            for p in prop.split():
                assert p in expected
        else:
            assert prop in expected

    for i in [-2, -1, 8, 9, .2599]:
        caught = False
        try:
            p = _Properties._type_from_index(i)
        except IndexError:
            caught = True
        assert caught


"""
def test_replace_in_fort3_file():
    replace_1 = Fort3Replacement(property='atom', new=True,
                                 content=['H', '1.298', '0.0'])
    out_path = replace_in_fort3(file_name, None, replace_1)
    assert os.path.abspath(out_path) == os.path.abspath(file_name) + '_new'
    assert os.path.exists(out_path) and os.path.isfile(out_path)
    os.remove(out_path)

    out_file = os.path.join(os.path.dirname(file_name), 'new_fort.3')
    out_path = replace_in_fort3(file_name, out_file, replace_1)
    assert os.path.abspath(out_file) == os.path.abspath(out_path)
    assert os.path.exists(out_path) and os.path.isfile(out_path)
    os.remove(out_path)
"""


def test_replace_in_fort3_count_property():
    replace_atom0 = Fort3Replacement(property='atom', new=True,
                                     content=['H', 1.298, 0.0])
    replace_atom1 = Fort3Replacement(property='atom', replace=True,
                                     content=['Ar', 3.001, 0.0])
    replace_atom2 = Fort3Replacement(property='atom', new=True,
                                     content=['O', 23.72, -1.0])
    replace_atom3 = Fort3Replacement(property='atom', new=True,
                                     content=['Be', 11.1, 2.1])

    replace_bond00 = Fort3Replacement(property='bond type', replace=True,
                                      content=['Ar', 'Ar', 3.5, 118.1])
    replace_bond01 = Fort3Replacement(property='bond type', new=True,
                                      content=['Ar', 'H', 5.1, 59.242])
    replace_bond33 = Fort3Replacement(property='bond type', new=True,
                                      content=['Be', 'Be', 1.2, 291.285])

    replace_angle000 = Fort3Replacement(property='bond angle', new=True,
                                        content=['Ar', 'Ar', 'Ar', 90, 300])
    replace_angle010 = Fort3Replacement(property='bond angle', new=True,
                                        content=['Ar', 'H', 'Ar', 65, 250])
    replace_angle112 = Fort3Replacement(property='bond angle', new=True,
                                        content=['O', 'O', 'Be', 85, 190])

    replace_torsion_0 = Fort3Replacement(
        property='torsion', new=True, content=['Ar', 'O', 'Be', 'H', 25, 190]
    )
    replace_torsion_1 = Fort3Replacement(
        property='torsion', new=True, content=['Ar', 'Ar', 'Be', 'Be', 10, 80]
    )

    replace_non_bond11 = Fort3Replacement(property='non bond', replace=True,
                                          content=['Ar', 'Ar', 1.1, 9.298])
    replace_non_bond01 = Fort3Replacement(property='non bond', new=True,
                                          content=['H', 'Ar', 0.23, 2.443])
    replace_non_bond22 = Fort3Replacement(property='non bond', new=True,
                                          content=['Be', 'Ar', 2.23, 1.295])

    all_replacements = (
        replace_atom0, replace_atom1, replace_atom2, replace_atom3,
        replace_bond00, replace_bond01, replace_bond33,
        replace_angle000, replace_angle010, replace_angle112,
        replace_torsion_0, replace_torsion_1,
        replace_non_bond01, replace_non_bond11, replace_non_bond22
    )
    counts = _count_property_instances(*all_replacements)

    assert counts[0] == 3
    assert counts[1] == 2
    assert counts[2] == 3
    assert counts[3] == 2
    assert counts[4] == 2
    return all_replacements


def test_replace_in_fort3_is_int():
    assert _is_int('2824')
    assert not _is_int('kdgkjg')
    assert _is_int(9285)
    assert not _is_int(2.52958)
    assert _is_int(-29859)
    assert _is_int('-29859')


def test_replace_in_fort3__count_existing_instances():
    counts = _count_existing_instances(file_name)
    assert counts[0] == 4
    assert counts[1] == 3
    assert counts[2] == 4
    assert counts[3] == 2
    assert counts[4] == 2


def test_replace_in_fort3_fort3_replacement_repr():
    r = Fort3Replacement(property='atom', new=True, content=['H', 1.008, 0.0])
    assert isinstance(repr(r), str)


def test_replace_in_fort3_parse_fort_3_file():
    tol = 1e-14
    atom_names, atoms, bonds, angles, torsions, non_bonds, scf, kappa, chi = (
        _parse_fort_3_file(file_name)
    )
    expected_names = ['O', 'H', 'Be', 'H+']
    for name in expected_names:
        assert name in atom_names.values()
    expected_masses = [15.999, 1.008, 9.012, 1.007]
    expected_charges = [0.0, 0.0, 0.0, 1.0]
    for name, mass, charge, atom in zip(expected_names, expected_masses,
                                        expected_charges, atoms):
        assert name == atom._content[0]
        assert mass == pytest.approx(atom._content[1], abs=tol)
        assert charge == pytest.approx(atom._content[2], abs=tol)

    expected_bonds = [(1, 1), (1, 2), (2, 4)]
    expected_bond_lengths = [3.21, 2.01, 5.98]
    expected_bond_eps = [2.4, 1.7, 8.8]
    for ind, length, eps, bond in zip(expected_bonds, expected_bond_lengths,
                                      expected_bond_eps, bonds):
        for a, b in zip(ind, bond._content[:2]):
            assert atom_names[a] == b
        assert bond._content[2] == pytest.approx(length, abs=tol)
        assert bond._content[3] == pytest.approx(eps, abs=tol)

    expected_bond_angles = [(1, 1, 1), (1, 2, 1), (3, 4, 3), (4, 4, 4)]
    expected_bond_theta = [75.0, 64.1, 90.9, 71.0]
    expected_bond_eps = [7.1, 4.0, 1.6, 17.2]
    for ind, theta, eps, angle in zip(expected_bond_angles,
                                      expected_bond_theta, expected_bond_eps,
                                      angles):
        for a, b in zip(ind, angle._content[:3]):
            assert atom_names[a] == b
        assert angle._content[3] == pytest.approx(theta, abs=tol)
        assert angle._content[4] == pytest.approx(eps, abs=tol)

    expected_torsions = [(1, 2, 3, 4), (2, 2, 2, 2)]
    expected_torsion_phi = [75.0, 12.5]
    expected_torsion_eps = [27.78, 0.24]
    for ind, theta, eps, torsion in zip(expected_torsions,
                                        expected_torsion_phi,
                                        expected_torsion_eps, torsions):
        for a, b in zip(ind, torsion._content[:4]):
            assert atom_names[a] == b
        assert torsion._content[4] == pytest.approx(theta, abs=tol)
        assert torsion._content[5] == pytest.approx(eps, abs=tol)

    expected_non_bonds = [(1, 1), (2, 2)]
    expected_non_bond_sigma = [1.8, 3.2]
    expected_non_bond_eps = [29.14, 2.349]
    for ind, sigma, eps, bond in zip(expected_non_bonds,
                                     expected_non_bond_sigma,
                                     expected_non_bond_eps, non_bonds):
        for a, b in zip(ind, bond._content[:2]):
            assert atom_names[a] == b
        assert bond._content[2] == pytest.approx(sigma, abs=tol)
        assert bond._content[3] == pytest.approx(eps, abs=tol)

    for m, expected in zip(scf, [5, 5, 10]):
        assert m == expected

    assert kappa == pytest.approx(1.204, abs=tol)

    expected_chi = [[0, 1,  0, -4],
                    [1, 0,  2,  0],
                    [0, 2,  0,  3],
                    [-4, 0,  3,  0]]
    assert np.allclose(expected_chi, chi)


def test_replace_in_fort3_sort_new_replace_args():
    tol = 1e-14
    atom_name, atoms, bonds, angles, torsions, non_bonds, scf, kappa, chi = (
        _parse_fort_3_file(file_name)
    )
    repl = (
        Fort3Replacement('atom', new=True, content=['P', 30.973, 0.0]),
        Fort3Replacement('atom', replace=True, content=['O', 16.000, 0.0]),
        Fort3Replacement('atom', new=True, content=['Ar-', 39.948, -1.0]),
    )
    atom_name, atoms, bonds, angles, torsions, non_bonds, scf, kappa, chi = (
        _sort_new_replace_args(atom_name, atoms, bonds, angles, torsions,
                               non_bonds, scf, kappa, chi, *repl)
    )
    assert len(atoms) == 6
    assert atoms[0]._content[0] == 'O'
    assert atoms[0]._content[1] == pytest.approx(16.0, abs=tol)
    for name, mass, charge in zip(['P', 'Ar-'], [30.973, 39.948], [0.0, -1.0]):
        found = False
        for atom in atoms[4:]:
            if name == atom._content[0]:
                found = True
                assert atom._content[1] == pytest.approx(mass, abs=tol)
                assert atom._content[2] == pytest.approx(charge, abs=tol)
        assert found

    print('', end='\n\n')
    for i, a in enumerate(atoms):
        print(i, a)
    print('', end='\n\n')

    # 1          O    15.999      0.0
    # 2          H     1.008      0.0
    # 3          Be    9.012      0.0
    # 4          H+    1.007      1.0
