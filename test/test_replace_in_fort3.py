import os
# import pytest
# from test.test_occam_data import _check_equal
# from test_occam_data import _check_equal
# from occamtools.replace_in_fort3 import (replace_in_fort3, Fort3Replacement,
#                                          _Properties)
from occamtools.replace_in_fort3 import (Fort3Replacement, replace_in_fort3,
                                         _Properties)


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
        except ValueError:
            caught = True
        assert caught


def test_replace_in_fort3_file():
    replace_1 = Fort3Replacement(property='atom', new=True,
                                 content=['H', '1.298', '0.0'])
    replace_2 = Fort3Replacement(property='atom', replace=True,
                                 content=['Ar', '3.298', '-1.0'])

    out_path = replace_in_fort3(file_name, None, replace_1, replace_2)

    if os.path.exists(out_path):
        os.remove(out_path)
