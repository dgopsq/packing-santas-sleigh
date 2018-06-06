import numpy as np

class Sleigh:
    def __init__(self, size):
        # Initialize matrix
        self.size = size
        self.matrix = np.zeros((self.size, self.size), dtype = np.int16)

        # N.B. We don't need to know how much free space
        # there is in a row, but I want to know the size
        # of each block of spaces.
        self.row_blocks = []

        for row in range(0, self.size):
            # (start_block, end_block)
            self.row_blocks.append([ (0, self.size) ])

    # Main function that execute the fittin process
    # for a particular present
    def fit_present(self, present):
        max_rotations = 3

        for y in range(0, self.size):
            for block in self.row_blocks[y]: 
                for rotation in range(0, max_rotations):
                    if((block[1] - block[0]) < present.x):
                        present.next_rotation()
                        continue

                    point = (block[0], y)

                    if(self.fit_from_point(present, point)):
                        self.add_present(present, point)
                        self.update_row_blocks(present, point)
                        present.set_point(point)
                        return True

                    present.next_rotation()

                present.set_default_rotation()

        return False

    # Function to see if a present fit from 
    # the top-left point.
    # present = Present object
    # point = (x, y)
    def fit_from_point(self, present, point):
        to_x = point[0] + present.x
        to_y = point[1] + present.y

        if(to_x > self.size or to_y > self.size):
            return False

        # Getting the relative sub-matrix from the layer matrix
        sub_layer = self.matrix[point[1]:to_y, point[0]:to_x]
        
        # Check if there are zeros
        return not np.count_nonzero(sub_layer)

    # Add a present to the Sleigh matrix
    # setting all the zeroes to the z size
    # of the present
    def add_present(self, present, point):
        for x in range(point[0], point[0] + present.x):
            for y in range(point[1], point[1] + present.y):
                self.matrix[y][x] = present.z

    # Update the blocks in each row
    def update_row_blocks(self, present, point):
        for y in range(point[1], point[1] + present.y):
            for index, block in enumerate(self.row_blocks[y]):
                item_block = (point[0], point[0] + present.x)

                if(item_block[0] < block[0] or item_block[0] > block[1]):
                    continue
                
                if(item_block[0] == block[0] and item_block[1] < block[1]):
                    self.row_blocks[y][index] = (item_block[1], block[1])
                elif(item_block[0] > block[0] and item_block[1] == block[1]):
                    self.row_blocks[y][index] = (block[0], item_block[0])
                else:
                    self.row_blocks[y].pop(index)
                    self.row_blocks[y].insert(index, (item_block[1], block[1]))
                    self.row_blocks[y].insert(index, (block[0], item_block[1]))