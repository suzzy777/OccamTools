import os
import sys
import pytest
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from read_fort7 import Fort7  # noqa: E402


def test_read_fort7_file():
    file_name = os.path.join(os.path.dirname(__file__), '..', 'data',
                             'example_fort.7')
    new_file_name = os.path.join(os.path.dirname(__file__), '..', 'data',
                                 'example_fort_new.7')

    fort7 = Fort7(file_name)
    fort7.read_file()
    assert fort7.title == 'example-fort.1'

    with open(file_name, 'r') as in_file, open(new_file_name, 'w') as out_file:
        for line in in_file:
            if 'title' in line:
                line = 'title: new_title\n'
            out_file.write(line)
    fort7 = Fort7(file_name)
    fort7.read_file(new_file_name)
    assert fort7.title == 'new_title'
    os.remove(new_file_name)
