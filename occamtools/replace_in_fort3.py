import os


class _Properties:
    ATOM_TYPE = 0
    BOND_TYPE = 1
    BOND_ANGLE = 2
    TORSION = 3
    NON_BONDED = 4
    SCF = 5
    COMPRESSIBILITY = 6
    CHI = 7

    @staticmethod
    def _type_from_index(index):
        for v in _Properties.__dict__:
            if not v.startswith('__'):
                if _Properties.__dict__[v] == index:
                    return v
        raise ValueError(f'Property index {index} not valid. Expected:\n'
                         '0 <= index <= 7')


class Fort3Replacement:
    def __init__(self, property=None, replace=None, new=None, content=None):
        self._content = content

        if property is not None:
            self._parse_property_name(property)
        else:
            self.property = property

        if isinstance(replace, bool) and isinstance(new, bool):
            if replace is new:
                raise ValueError('Replace and new cannot both be ' + str(new))
            else:
                self._new = new
                self._replace = replace
        elif isinstance(replace, bool) or isinstance(new, bool):
            if isinstance(replace, bool):
                self._replace = replace
                self._new = not replace
            else:
                self._new = new
                self._replace = not new
        elif (new is None) and (replace is None):
            self._new = new
            self._replace = replace
        else:
            raise TypeError('Expected None or bool for new and replace, not '
                            + str(type(new)) + ' and ' + str(type(replace)))

    @property
    def new(self):
        return self._new

    @new.setter
    def new(self, new):
        if not isinstance(new, bool):
            raise TypeError('Expected bool for new, got ' + str(type(new)))
        self._new = new
        self._replace = not new

    @property
    def replace(self):
        return self._replace

    @replace.setter
    def replace(self, replace):
        if not isinstance(replace, bool):
            raise TypeError('Expected bool for replace, got '
                            + str(type(replace)))
        self._replace = replace
        self._new = not replace

    def _parse_property_name(self, property):
        p = property.lower()
        if 'atom' in p:
            self.property = _Properties.ATOM_TYPE
        elif 'bond' in p and 'type' in p:
            self.property = _Properties.BOND_TYPE
        elif 'bond' in p and 'ang' in p:
            self.property = _Properties.BOND_ANGLE
        elif 'torsion' in p:
            self.property = _Properties.TORSION
        elif 'non' in p and 'bond' in p:
            self.property = _Properties.NON_BONDED
        elif 'scf' in p or 'hpf' in p:
            self.property = _Properties.SCF
        elif 'comp' in p:
            self.property = _Properties.COMPRESSIBILITY
        elif 'chi' in p:
            self.property = _Properties.CHI
        else:
            error_string = ('Property string ' + property + ' was not'
                            ' recognized')
            raise ValueError(error_string)

    def __repr__(self):
        prop_type = _Properties._type_from_index(self.property)
        return (f'Fort3Replacement(property={prop_type}, '
                f'replace={self._replace}, new={self._new}, '
                f'content={self._content})')


def _count_property_instances(*args):
    print("\n")
    for prop in args:
        print(prop)
    print("\n")


def replace_in_fort3(input_file, output_path, *args):
    """Replace or add to an existing fort.3 file

    The output file is named <input_file_name>_new by default, if no other
    output name is supplied.

    The replacement specification is done using Fort3Replacement instances,
    any number of which may be given as positional arguments
    """
    if (output_path is None) or (output_path == ''):
        output_path = os.path.join(os.path.dirname(input_file),
                                   input_file + '_new')

    with open(input_file, 'r') as in_file, open(output_path, 'w') as out_file:
        _count_property_instances(*args)

        for i, line in enumerate(in_file):
            out_file.write(line)

    return output_path
