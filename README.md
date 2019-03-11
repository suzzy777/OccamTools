[![occam-website](http://www.occammd.org/wp-content/uploads/2018/08/cropped-Untitled-2-01-2.png)](http://www.occammd.org/)

[![Build Status](https://travis-ci.com/mortele/OccamTools.svg?token=81VUNKkUYjZSicZzs1NR&branch=master)](https://travis-ci.com/mortele/OccamTools) [![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/b91377a289bc42868314310dd6be2b60)](https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=mortele/OccamTools&amp;utm_campaign=Badge_Grade) [![codecov](https://codecov.io/gh/mortele/OccamTools/branch/master/graph/badge.svg?token=IXlriBpSwo)](https://codecov.io/gh/mortele/OccamTools) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## OccamTools
Analysis and synthesis tools for OCCAM molecular dynamics/hybrid particle-field simulations.

### Development build
Clone the repository
```bash
> git clone git@github.com:mortele/OccamTools.git
> cd OccamTools
```
create a virtualenv named `ot` 
```bash
> pip3 install virtualenv
> virtualenv ot
> source ot/bin/activate 
```
install the `occamtools` package in `--editable` (or `-e` mode) by
```bash
> pip3 install -e .
```
Functions and classes in scripts in the `occamtools` and `test` directories may now be imported by simply 
```python
from occamtools.filename import class_name
from occamtools.filename import function_name
from test.filename import test_function_name
```
#### Exiting `virtualenv`
Exit the pip virtual environment by
```bash
> deactivate
```