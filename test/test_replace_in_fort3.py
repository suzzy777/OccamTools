import os
# import pytest
# from test.test_occam_data import _check_equal
# from test_occam_data import _check_equal
from occamtools.replace_in_fort3 import (Fort3Replacement, replace_in_fort3,
                                         _Properties, _is_int,
                                         _count_property_instances,
                                         _count_existing_instances,
                                         _parse_fort_3_file)


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


def test_replace_in_fort3_parse_fort_3_file():
    all_replacements = test_replace_in_fort3_count_property()
    replace_atoms = all_replacements[0:4]
    replace_bonds = all_replacements[4:7]
    replace_angles = all_replacements[7:10]
    replace_torsions = all_replacements[10:12]
    replace_non_bonds = all_replacements[12:]

    ret = _parse_fort_3_file(file_name)
