import os
import numpy as np


def generate_uniform_random(n_particles, box, path=''):
    if os.path.isdir(path):
        file_name = os.path.join(path, 'fort.5')
    else:
        file_name = path

    xBox = box[0]
    yBox = box[1]
    zBox = box[2]

    with open(file_name, 'w') as out_file:
        x = np.random.uniform(low=0.0, high=xBox, size=(n_particles))
        y = np.random.uniform(low=0.0, high=yBox, size=(n_particles))
        z = np.random.uniform(low=0.0, high=zBox, size=(n_particles))

        out_file.write('Box:\n')
        out_file.write('{x:10.5f} {y:10.5f} {z:10.5f} {s:10.5f}\n'.format(
            x=box[0], y=box[1], z=box[2], s=0.0
        ))

        out_file.write('Number of particles:\n')
        out_file.write(f'{n_particles}\n')

        for i in range(n_particles):
            atoms_per_mol = 1
            label = 'Ar'
            label_index = 1
            n_bonds = 0
            bond1, bond2, bond3, bond4, bond5, bond6 = [0 for i in range(6)]
            out_file.write(f'Molecule # {i+1}\n')
            out_file.write(f'{atoms_per_mol}\n')
            out_file.write(f'{i+1} {label} {label_index} {n_bonds} ')
            out_file.write(f'{x[i]} {y[i]} {z[i]}')
            out_file.write(f'{bond1} {bond2} {bond3} {bond4} {bond5} {bond5}')
            out_file.write('\n')
