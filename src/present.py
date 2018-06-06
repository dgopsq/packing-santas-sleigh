import numpy as np

class Present:
    def __init__(self, pid, x, y, z):
        self.pid = np.int32(pid)
        self.x = np.int16(x)
        self.y = np.int16(y)
        self.z = np.int16(z)

        # The starting point used
        # to compute the output file
        self.point = False

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

    # _NOT IMPLEMENTED_
    # Rotate the present
    def rotate(self):
        return False