import numpy as np

class Present:
    def __init__(self, pid, x, y, z):
        self.pid = np.int32(pid)
        self.x = np.int16(x)
        self.y = np.int16(y)
        self.z = np.int16(z)

    # _NOT IMPLEMENTED_
    # Rotate the present
    def rotate(self):
        return False