import os
import numpy as np
import itertools as it


def _check_if_path(path, append='fort.5'):
    if os.path.isdir(path):
        file_name = os.path.join(path, append)
    else:
        file_name = path
    return file_name


def _write_box(out_file, box, scaling=0.0):
    out_file.write('Box:\n')
    out_file.write('{x:.15f} {y:.15f} {z:.15f} {s:.15f}\n'.format(
        x=box[0], y=box[1], z=box[2], s=scaling
    ))


def _write_n_particles(out_file, n_particles):
    out_file.write('Number of particles:\n')
    out_file.write(f'{n_particles}\n')


def _fcc_unit_cell(x, y, z, lattice_constant):
    r1 = 0.5 * lattice_constant * np.asarray([0, 0, 0])
    r2 = 0.5 * lattice_constant * np.asarray([1, 1, 0])
    r3 = 0.5 * lattice_constant * np.asarray([0, 1, 1])
    r4 = 0.5 * lattice_constant * np.asarray([1, 0, 1])
    return r1, r2, r3, r4


def _write_molecule(out_file, number, x, y, z, atoms_per_mol=1, label='Ar',
                    label_index=1, velocity=False, n_bond=0,
                    bond1=0, bond2=0, bond3=0, bond4=0, bond5=0, bond6=0):
    out_file.write(f'Molecule # {number}\n')
    out_file.write(f'{atoms_per_mol}\n')
    out_file.write(f'{number} {label} {label_index} {n_bond} ')
    out_file.write(f'{x:.15f} {y:.15f} {z:.15f} ')
    if velocity:
        vx, vy, vz = [0, 0, 0]
        out_file.write(f'{vx} {vy} {vz} ')

    out_file.write(f'{bond1} {bond2} {bond3} {bond4} {bond5} {bond6}')
    out_file.write('\n')


def _generate_uniform_random_stable(n_particles, box, max_iter=1000,
                                    threshold=0.2):
    x_box, y_box, z_box = box
    x = np.random.uniform(low=0.0, high=x_box, size=(n_particles))
    y = np.random.uniform(low=0.0, high=y_box, size=(n_particles))
    z = np.random.uniform(low=0.0, high=z_box, size=(n_particles))
    dist = np.zeros(shape=(n_particles, n_particles))
    for iter in range(1, max_iter+1):
        for i, (xi, yi, zi) in enumerate(zip(x, y, z)):
            for j, (xj, yj, zj) in enumerate(zip(x, y, z)):
                dist[i, j] = (xj - xi)**2 + (yj - yi)**2 + (zj - zi)**2
        max_dist = np.max(np.max(dist))
        if max_dist < threshold**2:
            break
        if iter == max_iter:
            error_str = (f'Unable to find a relaxed configuration of '
                         f'{n_particles} particles in {max_iter} iterations. '
                         f'Max distance found: {max_dist} > the threshold '
                         f' set to {threshold}.')
            raise RuntimeError(error_str)
        for (i, j), d in np.ndenumerate(dist):
            if d < threshold**2:
                pj = np.random.uniform(low=0.0, high=1.0, size=(3))
                x[j] = pj[0] * x_box
                y[j] = pj[1] * y_box
                z[j] = pj[2] * z_box
    return x, y, z


def generate_uniform_random(n_particles, box, path='', stable=False, **kwargs):
    if stable:
        x_stable, y_stable, z_stable = (
            _generate_uniform_random_stable(n_particles, box, **kwargs)
        )
    file_name = _check_if_path(path)

    x_box, y_box, z_box = box

    with open(file_name, 'w') as out_file:
        if not stable:
            x = np.random.uniform(low=0.0, high=x_box, size=(n_particles))
            y = np.random.uniform(low=0.0, high=y_box, size=(n_particles))
            z = np.random.uniform(low=0.0, high=z_box, size=(n_particles))
        else:
            x = x_stable
            y = y_stable
            z = z_stable

        _write_box(out_file, box)
        _write_n_particles(out_file, n_particles)

        for i in range(n_particles):
            _write_molecule(out_file, i+1, x[i], y[i], z[i])


def generate_fcc(cell_box, lattice_constant, velocity=False, path=''):
    file_name = _check_if_path(path)
    x_box, y_box, z_box = cell_box

    # Make sure the cell_box argument consists of only positive integers or
    # positive floats with .0 appended.
    if (any([x != int(x) for x in cell_box])
            or any([x < 0 for x in cell_box])):
        raise ValueError("The cell_box can only contain positive integers, not"
                         f" [{cell_box[0]} {cell_box[1]} {cell_box[2]}].")
    b = lattice_constant
    n_particles = 4 * x_box * y_box * z_box

    with open(file_name, 'w') as out_file:
        _write_box(out_file, b * np.asarray(cell_box))
        _write_n_particles(out_file, n_particles)

        atom_counter = 1
        for (i, j, k) in it.product(range(int(x_box)),
                                    range(int(y_box)),
                                    range(int(z_box))):
            x, y, z = [b * dim for dim in (i, j, k)]
            R = _fcc_unit_cell(x, y, z, b)

            for l in range(4):
                r = R[l]
                xi, yj, zk = np.asarray(r) + np.asarray([x, y, z])

                _write_molecule(out_file, atom_counter, xi, yj, zk,
                                velocity=velocity)
                atom_counter += 1
    return n_particles
