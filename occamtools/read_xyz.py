import numpy as np


def _are_floats(*args):
    are_floats = True
    try:
        for f in args:
            _ = float(f)
    except TypeError:
        are_floats = False
    return are_floats


class Xyz:
    def __init__(self, file_name):
        self.file_name = file_name

    def _allocate_arrays(self):
        self.type = np.zeros(self.n_particles)
        self.time = np.zeros(self.n_time_steps)
        self.x = np.zeros(shape=(self.n_time_steps, self.n_particles))
        self.y = np.zeros(shape=(self.n_time_steps, self.n_particles))
        self.z = np.zeros(shape=(self.n_time_steps, self.n_particles))

    def _parse_comment_first(self, line):
        sline = line.split()
        recognized = True
        self.box = [None, None, None]
        if len(sline) == 4:
            if not _are_floats(*tuple(sline)):
                recognized = False
            else:
                self.time[0] = float(sline[0])
                self.box = [float(sline[1]), float(sline[2]), float(sline[3])]
        elif len(sline) == 3:
            if not _are_floats(*tuple(sline)):
                recognized = False
            else:
                self.box = [float(sline[0]), float(sline[1]), float(sline[2])]
        else:
            recognized = False
        return recognized

    def _parse_types(self, in_file):
        in_file.seek(0)  # Reset position to the start of the file
        self.type_dict = {}
        ind = 0
        for _ in range(2):
            line = in_file.readline()
        for i in range(self.n_particles):
            line = in_file.readline().split()
            t = line[0]
            if t not in self.type_dict:
                self.type_dict[t] = ind
                ind += 1
            self.type[i] = self.type_dict[t]

    def read_file(self, file_name=None, save=True):
        if file_name is not None:
            self.file_name = file_name

        # Go through the file initally and just count the number of lines.
        self.num_lines = sum(1 for line in open(self.file_name, 'r'))

        with open(self.file_name, 'r') as in_file:
            self.n_particles = int(in_file.readline())
            self.n_time_steps = self.num_lines // self.n_particles
            self._allocate_arrays()
            line = in_file.readline()
            self.comment_format_known = self._parse_comment_first(line)
            self._parse_types(in_file)

            in_file.seek(0)
            for time_step in range(self.n_time_steps):
                for _ in range(2):
                    line = in_file.readline()
                if self.comment_format_known:
                    self.time[time_step] = float(line.split()[0])
                for i in range(self.n_particles):
                    line = in_file.readline().split()
                    self.x[time_step, i] = float(line[1])
                    self.y[time_step, i] = float(line[2])
                    self.z[time_step, i] = float(line[3])
