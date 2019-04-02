import os
import numpy as np


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
        raise IndexError(f'Property index {index} not valid. Expected:\n'
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
    counts = {key: 0 for key in range(5)}
    for p in args:
        if (p.new is True) and (p.property <= 4):
            counts[p.property] += 1
    return counts


def _is_int(s):
    try:
        s = float(s)
        if s.is_integer():
            return True
        else:
            return False
    except ValueError:
        return False


def _count_existing_instances(fort_file):
    keys = ['atom types', 'bond types', 'bond angles', 'torsions', 'non-bond']
    counts = {key: 0 for key in range(5)}
    with open(fort_file, 'r') as in_file:
        for line in in_file:
            sline = line.split()
            if len(sline) > 1:
                if _is_int(sline[0]):
                    for i, key in enumerate(keys):
                        if key in line:
                            counts[i] = int(sline[0])
                            break
    return counts


def _parse_fort_3_file(fort_file):
    atom_name = {}
    atoms = []
    bonds = []
    angles = []
    torsions = []
    non_bonds = []

    with open(fort_file, 'r') as in_file:
        for _ in range(4):
            line = in_file.readline()
        while '*****' not in line:  # atom types
            index, name, mass, charge = line.split()
            index, mass, charge = int(index), float(mass), float(charge)
            atom_name[index] = name
            atoms.append(Fort3Replacement(property='atom', new=True,
                                          content=[name, mass, charge]))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # bond types
            index_1, index_2, sigma, eps = line.split()
            index_1, index_2 = int(index_1), int(index_2)
            sigma, eps = float(sigma), float(eps)
            content = [atom_name[index_1], atom_name[index_2], sigma, eps]
            bonds.append(Fort3Replacement(property='bond type', new=True,
                                          content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # bond angles
            ind1, ind2, ind3, theta, eps = line.split()
            ind1, ind2, ind3 = (int(i) for i in (ind1, ind2, ind3))
            theta, eps = float(theta), float(eps)
            content = [atom_name[ind1], atom_name[ind2], atom_name[ind3],
                       theta, eps]
            angles.append(Fort3Replacement(property='bond angle', new=True,
                                           content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # torsions
            ind1, ind2, ind3, ind4, phi, eps = line.split()
            ind1, ind2, ind3, ind4 = (int(i) for i in (ind1, ind2, ind3, ind4))
            phi, eps = float(phi), float(eps)
            content = [atom_name[ind1], atom_name[ind2], atom_name[ind3],
                       atom_name[ind4], phi, eps]
            torsions.append(Fort3Replacement(property='bond angle', new=True,
                                             content=content))
            line = in_file.readline()

        for _ in range(3):
            line = in_file.readline()
        while '******' not in line:  # non-bonded interactions
            index_1, index_2, sigma, eps = line.split()
            index_1, index_2 = int(index_1), int(index_2)
            sigma, eps = float(sigma), float(eps)
            content = [atom_name[index_1], atom_name[index_2], sigma, eps]
            non_bonds.append(Fort3Replacement(property='non bonded', new=True,
                                              content=content))
            line = in_file.readline()

        for _ in range(2):
            line = in_file.readline()
        scf = [int(i) for i in line.split()]
        for _ in range(2):
            line = in_file.readline()
        kappa = float(line)
        line = in_file.readline()
        chi = np.empty(shape=(len(atom_name), len(atom_name)))
        for i in range(chi.shape[1]):
            sline = in_file.readline().split()
            chi[i, :] = np.asarray([float(s) for s in sline])

        return (atom_name, atoms, bonds, angles, torsions, non_bonds, scf,
                kappa, chi)


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

    fort3 = _parse_fort_3_file(input_file)
    with open(input_file, 'r') as in_file:
        new_counts = _count_property_instances(*args)
        existing_counts = _count_existing_instances(input_file)
        total = {key: new_counts[key] + existing_counts[key]
                 for key in new_counts}

    return output_path
