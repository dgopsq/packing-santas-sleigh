import numpy as np
import itertools as it

class Present:
    def __init__(self, pid, x, y, z):
        self.pid = np.int32(pid)
        self.x = np.int16(x)
        self.y = np.int16(y)
        self.z = np.int16(z)

        # The starting point used
        # to compute the output file
        self.point = False

        # Combinations of rotations
        self.combinations = []
        self._generate_combinations()

        # (?) Optimize z
        self.set_default_rotation()

    # Set the starting point in 
    # the matrix
    def set_point(self, point):
        self.point = point

    # Generate output list used
    # to validate the result
    def generate_output_list(self):
        if(self.point == False):
            return []
        
        output = []

        output += [self.pid.item()] 

        # When there is only self.point, one unit is added
        # to fix the starting point of the algorithm
        output += [self.point[0] + 1, self.point[1] + 1, 1] 
        output += [(self.point[0] + self.x).item(), self.point[1] + 1, 1]
        output += [(self.point[0] + self.x).item(), (self.point[1] + self.y).item(), 1]
        output += [self.point[0] + 1, (self.point[1] + self.y).item(), 1]

        output += [self.point[0] + 1, self.point[1] + 1, self.z.item()] 
        output += [(self.point[0] + self.x).item(), self.point[1] + 1, self.z.item()]
        output += [(self.point[0] + self.x).item(), (self.point[1] + self.y).item(), self.z.item()]
        output += [self.point[0] + 1, (self.point[1] + self.y).item(), self.z.item()]

        return output

    # We want the present in the position
    # with less z height.
    def set_default_rotation(self):
        current = (self.x, self.y, self.z)
        new = self.combinations[0]
        
        self._sort_combinations()

        if(current[2] > new[2]):
            self.next_rotation()
            self._sort_combinations()

    # Get the next rotation (the best in
    # terms of z height).
    def next_rotation(self):
        old = (self.x, self.y, self.z)
        self.combinations.append(old)
        self.x, self.y, self.z = self.combinations.pop(0)

    def _generate_combinations(self):
        main = (self.x, self.y, self.z)
        self.combinations = list(it.permutations(main))
        self._sort_combinations()
        
    def _sort_combinations(self):
        self.combinations = sorted(self.combinations, key = lambda x: x[2])