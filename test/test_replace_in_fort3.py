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
    print("\n\n\n")

    properties = ['atom', 'bond type', 'bond angle', 'torsion', 'non bonded',
                  'scf', 'compress', 'chi']
    indices = [i for i in range(len(properties))]

    for prop, index in zip(properties, indices):
        replacement = Fort3Replacement(property=prop)
        assert replacement.property == index

    print("\n\n\n")
