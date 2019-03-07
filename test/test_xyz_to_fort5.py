import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
# from xyz_to_fort5 import (xyz_to_fort5, _check_box,
#                           _parse_comment_line)  # noqa: E402
from xyz_to_fort5 import _parse_comment_line  # noqa: E402


def test_xyz_to_occam_parse_comment_line():
    lines = ['125.0 25.0 25.0',
             '#125.000000000000000   25.000000000000000   25.000000000000000',
             '# 125.000000000000000   25.000000000000000   25.000000000000000',
             '# 125 25 25',
             '#125 25 25',
             '#box:125.000000000000000   25.000000000000000   25.000000000000',
             '#box:125 25 25',
             '#box:125.0 25 25',
             '#box: 125.000000000000000   25.000000000000000   25.00000000000',
             '#box:125 25.0 25',
             '# box:125.000000000000000   25.000000000000000   25.00000000000',
             '# box:125   25   25',
             '# box:125   25.000   25',
             '# box: 125   25   25',
             '# box:  125.000000000000000   25.000000000000000   25.000000000']
    expected = [125.0, 25.0, 25.0]
    for line in lines:
        box = _parse_comment_line(line)
        assert box == pytest.approx(expected, abs=1e-15)
