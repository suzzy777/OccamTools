import numpy as np


class Fort7:
    def __init__(self, file_name):
        self.file_name = file_name

    def _allocate_arrays(self):
        self.step = np.zeros(self.n_time_steps)
        self.kinetic_energy = np.zeros(self.n_time_steps)
        self.potential_energy = np.zeros(self.n_time_steps)
        self.temperature = np.zeros(self.n_time_steps)
        self.pressure = np.zeros(self.n_time_steps)
        self.pressure_nb = np.zeros(self.n_time_steps)
        self.pressure_pf_0 = np.zeros(self.n_time_steps)
        self.pressure_pf_1 = np.zeros(self.n_time_steps)

    def _prune_arrays(self):
        i = self.current_index
        self.step = self.step[:i]
        self.kinetic_energy = self.kinetic_energy[:i]
        self.potential_energy = self.potential_energy[:i]
        self.temperature = self.temperature[:i]
        self.pressure = self.pressure[:i]
        self.pressure_nb = self.pressure_nb[:i]
        self.pressure_pf_0 = self.pressure_pf_0[:i]
        self.pressure_pf_1 = self.pressure_pf_1[:i]

    def _parse_cycle(self, in_file):
        self.current_index = 0
        while self._parse_step(in_file):
            self.current_index += 1
        self._prune_arrays()
        self._parse_final_avg(in_file)

    def _parse_step(self, in_file):
        i = self.current_index
        while True:
            line = in_file.readline().strip().split()
            if line:  # Make sure the line isnt empty, ''
                if 'nonbonded virial' in ' '.join(line):
                    return True
                if '****' in ' '.join(line):
                    return False

                if 'step no' in ' '.join(line):
                    self.step[i] = int(line[-1])
                elif 'ekin' in line[-1]:
                    self.kinetic_energy[i] = float(line[1])
                elif 'epot shifted' in ' '.join(line):
                    self.potential_energy[i] = float(line[1])
                elif 'temp' in line[-1]:
                    self.temperature[i] = float(line[1])
                elif line[-1] == 'press':
                    self.pressure[i] = float(line[1])
                elif 'PP_press_' in ' '.join(line):
                    self.pressure_nb[i] = float(line[1])
                elif 'PF_press_0' in ' '.join(line):
                    self.pressure_pf_0[i] = float(line[1])
                elif 'PF_press_1' in ' '.join(line):
                    self.pressure_pf_1[i] = float(line[1])

    def _parse_final_avg(self, in_file):
        pass

    def read_file(self, file_name=None):
        if file_name is not None:
            self.file_name = file_name
        with open(self.file_name, 'r') as in_file:
            while True:
                line = in_file.readline()
                line = line.split()
                if line:  # Make sure the line isnt empty, ''
                    if 'title' in line[0]:
                        self.title = line[1].strip()
                    elif 'number of atoms' in line[0]:
                        self.n_particles = int(line[1].strip())
                    elif 'cutoff' in line[0]:
                        self.cutoff = float(line[-1].strip())
                    elif 'box' in line[0]:
                        line = in_file.readline().split()
                        self.box = [float(b) for b in line]
                    elif 'number of time steps' in ' '.join(line):
                        self.n_time_steps = int(line[-1])
                    elif 'time step length' in ' '.join(line):
                        self.dt = float(line[-1])
                    elif 'MDCYCLE' in line:
                        break
            self._allocate_arrays()
            self._parse_cycle(in_file)
