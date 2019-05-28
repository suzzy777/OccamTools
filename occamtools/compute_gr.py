import numpy as np
from occamtools.replace_in_fort3 import _is_int
from occamtools import OccamData


def _gr_kernel(x, y, z, bx, by, bz, n_atoms):
    r = np.empty(int(n_atoms * (n_atoms - 1) / 2))
    ind = 0
    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            dx = x[j] - x[i]
            if (dx > bx * 0.5):
                dx = dx - bx
            if (dx <= - bx * 0.5):
                dx = dx + bx

            dy = y[j] - y[i]
            if (dy > by * 0.5):
                dy = dy - by
            if (dy <= - by * 0.5):
                dy = dy + by

            dz = z[j] - z[i]
            if (dz > bz * 0.5):
                dz = dz - bz
            if (dz <= - bz * 0.5):
                dz = dz + bz

            r[ind] = np.sqrt(dx*dx + dy*dy + dz*dz)
            ind += 1
    return r


def compute_gr(data, steps=None, **kwargs):
    if not isinstance(data, OccamData):
        error_str = (f'Given data must be of type OccamData, not {type(data)}')
        raise TypeError(error_str)

    box = data.box
    x, y, z = data.x, data.y, data.z
    n_time_steps, n_atoms = x.shape

    if steps is None:
        steps = range(n_time_steps)
    elif _is_int(steps):
        steps = [steps]
    else:
        steps = range(steps[0], steps[1]+1)

    for step in steps:
        print(step)
        r = _gr_kernel(x[step, :], y[step, :], z[step, :],
                       box[0], box[1], box[2], n_atoms)
        hist, bins = np.histogram(r, **kwargs)
        density = n_atoms / (box[0] * box[1] * box[2])
        bins_adj = bins + np.mean(np.diff(bins)) / 2
        volume_bins = (4/3) * np.pi * (bins_adj[1:]**3 - bins_adj[:-1]**3)

        print(bins, volume_bins)
        hist = hist.astype(float) / (volume_bins * density)
    return hist, bins
