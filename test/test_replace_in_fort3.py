# import os
# import pytest
# from test.test_occam_data import _check_equal
# from test_occam_data import _check_equal
# from occamtools.replace_in_fort3 import (replace_in_fort3, Fort3Replacement,
#                                          _Properties)
from occamtools.replace_in_fort3 import Fort3Replacement


# file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
#                          'example_fort.3')


def test_replace_in_fort3_properties():
    properties = ['atom', 'bond type', 'bond angle', 'torsion', 'non bonded',
                  'scf', 'compress', 'chi']
    indices = [i for i in range(len(properties))]

    for prop, index in zip(properties, indices):
        replacement = Fort3Replacement(property=prop)
        assert replacement.property == index
    replacement = Fort3Replacement()
    assert replacement.property is None

    replacement = Fort3Replacement(new=True)
    assert replacement.new is True
    assert replacement.replace is False

    replacement.replace = True
    assert replacement.new is False
    assert replacement.replace is True

    for inp in ['string', 1, 8.251, int]:
        caught = False
        try:
            replacement.new = inp
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
