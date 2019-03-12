import numpy as np
from occamtools.xyz_to_fort5 import _parse_comment_line


class Xyz:
    def __init__(self, file_name):
        self.file_name = file_name

    def _allocate_arrays(self):
        self.type = np.zeros(self.n_particles)
        self.x = np.zeros(shape=(self.n_time_steps, self.n_particles))
        self.y = np.zeros(shape=(self.n_time_steps, self.n_particles))
        self.z = np.zeros(shape=(self.n_time_steps, self.n_particles))

    def _parse_comment(self, line):
        sline = line.split()
        if len(sline) == 4:
            line = ' '.join(sline[:-1])
        return _parse_comment_line()

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

    def read_file(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name

        # Go through the file initally and just count the number of lines.
        self.num_lines = sum(1 for line in open(self.file_name, 'r'))

        with open(self.file_name, 'r') as in_file:
            self.n_particles = int(in_file.readline())
            self.n_time_steps = self.num_lines // self.n_particles
            self._allocate_arrays()
            self._parse_types(in_file)

            in_file.seek(0)
            for time_step in range(self.n_time_steps):
                for _ in range(2):
                    line = in_file.readline()
                for i in range(self.n_particles):
                    line = in_file.readline().split()
                    self.x[time_step, i] = float(line[1])
                    self.y[time_step, i] = float(line[2])
                    self.z[time_step, i] = float(line[3])
