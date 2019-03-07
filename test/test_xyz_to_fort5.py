import os
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
# from xyz_to_fort5 import (xyz_to_fort5, _check_box,
#                           _parse_comment_line)  # noqa: E402
from xyz_to_fort5 import _parse_comment_line, _check_box  # noqa: E402


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


def test_check_box():
    box = [5.29589528, 295.29859815, 21.95820590]
    box_mod = [b for b in box]
    box_mod[0] = box_mod[0] + 1e-3
    caught_none = False
    try:
        _check_box(None, None)
    except ValueError:
        caught_none = True
    assert caught_none

    caught_diff = False
    try:
        _check_box(box, box_mod)
    except ValueError:
        caught_diff = True
    assert caught_diff

    caught_no = False
    try:
        _check_box(box, box)
    except ValueError:
        caught_no = True
    assert not caught_no
