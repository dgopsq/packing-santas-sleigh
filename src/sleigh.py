import numpy as np

class Sleigh:
    def __init__(self, size_x, size_y):
        # Initialize matrix
        self.size_x = size_x
        self.size_y = size_y
        self.level = 0
        self.matrix = np.zeros((self.size_y, self.size_x), dtype = np.int16)
        self.max_space = float(self.size_x * self.size_y)

        # - PARAMETERS -
        # Here it's possible to change useful parameters
        self.max_present_rotations = 5
        self.min_block_size = 3
        self.max_space_treshold = 0.3
        self.min_space_treshold = 0.6

        # N.B. We don't need to know how much free space
        # there is in a row, but I want to know the size
        # of each block of spaces.
        self.row_blocks = []

        for row in range(0, self.size_y):
            # (start_block, end_block)
            self.row_blocks.append([ (0, self.size_x - 1) ])

    # Main function that execute the fittin process
    # for a particular present.
    # If we are iterating over the reversed matrix
    # we should remember that only the iteration for y
    # starts from the last item, the iteration for x
    # is still from left to right.
    def fit_present(self, present, rotate_matrix = False):
        y_range = range(0, self.size_y)

        if(rotate_matrix):
            y_range = reversed(y_range)

        for y in y_range:
            for block in self.row_blocks[y]: 
                for rotation in range(0, self.max_present_rotations):
                    if((block[1] - block[0] + 1) < present.x):
                        present.next_rotation()
                        continue

                    if(rotate_matrix):
                        # If the real y is out of the sleight
                        # then refuse the package
                        if(y - present.y + 1 < 0):
                            present.next_rotation()
                            continue

                        point = (block[0], y - present.y + 1, self.level)
                    else:
                        point = (block[0], y, self.level)

                    if(self.fit_from_point(present, point)):
                        self.add_present(present, point)
                        self.update_row_blocks(present, point)
                        return point

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

        if(to_x > self.size_x or to_y > self.size_y):
            return False

        # Getting the relative sub-matrix from the layer matrix
        sub_layer = self.matrix[point[1]:to_y, point[0]:to_x]
        
        # Check if there are zeros
        return not np.count_nonzero(sub_layer)

    # Add a present to the Sleigh matrix
    # setting all the zeroes to the z size
    # of the present.
    def add_present(self, present, point):
        for x in range(point[0], point[0] + present.x):
            for y in range(point[1], point[1] + present.y):
                self.matrix[y][x] = present.z

    # Update the blocks in each row by splitting them.
    # There is a block size limit which is at least
    # the "min_block_size" variable value.
    def update_row_blocks(self, present, point):

        # This mens that block of size n will be
        # removed and ignored.
        min_block_size = self.min_block_size

        for y in range(point[1], point[1] + present.y):
            for index, block in enumerate(self.row_blocks[y]):
                item_block = (point[0], point[0] + present.x - 1)

                if(item_block[0] < block[0] or item_block[0] > block[1]):
                    continue
                
                # Item to add is near the left edge of the block
                if(item_block[0] == block[0] and item_block[1] < block[1]):
                    if(block[1] - item_block[1] < min_block_size):
                        self.row_blocks[y].pop(index)
                    else:
                        self.row_blocks[y][index] = (item_block[1] + 1, block[1])
                # Item to add is near the right edge of the block
                elif(item_block[0] > block[0] and item_block[1] == block[1]):
                    if(item_block[0] - block[0] < min_block_size):
                        self.row_blocks[y].pop(index)
                    else:
                        self.row_blocks[y][index] = (block[0], item_block[0] - 1)
                # Item to add is  NOT near an edge of the block
                elif(item_block[0] > block[0] and item_block[1] < block[1]):
                    self.row_blocks[y].pop(index)

                    if(block[1] - item_block[1] >= min_block_size):
                        self.row_blocks[y].insert(index, (item_block[1] + 1, block[1]))

                    if(item_block[0] - block[0] >= min_block_size):
                        self.row_blocks[y].insert(index, (block[0], item_block[0] - 1))
                # else...
                elif(item_block[0] == block[0] and item_block[1] == block[1]):
                    self.row_blocks[y].pop(index)
    
    # Update the sleigh matrix and
    # add a level. It actually starts
    # fitting presents to z + 1.
    def next_level(self):
        self.level += 1
        substract_matrix = np.full((self.size_y, self.size_x), 1, dtype = np.int16)
        self.matrix = self.matrix - substract_matrix
        self.matrix = self.matrix.clip(min = 0)

    # We want a level that has enough free
    # space to add out packages.
    # This is not a great move, but probably allows
    # to reduce time.
    def next_operable_level(self):
        # Go to next level
        self.next_level()

        if(self.is_level_operable()):
            return self.level
        else:
            # No, so to the next level!
            self.next_operable_level()

    # This method checks if the current
    # level has enough free space
    def is_level_operable(self):
        # Get space percentage
        free_space = (self.max_space - np.count_nonzero(self.matrix)) / self.max_space

        return free_space > self.min_space_treshold

    # This method checks if it's time
    # to switch level.
    def is_time_to_change(self):
        # Get space percentage
        free_space = (self.max_space - np.count_nonzero(self.matrix)) / self.max_space

        return free_space < self.max_space_treshold

    # Update blocks list. Because we change
    # levef for a reason!
    def recompute_blocks(self):
        self.row_blocks = []

        # This mens that block of size n will be
        # removed and ignored.
        min_block_size = self.min_block_size

        for y in range(0, self.size_y):
            n_free = 0

            self.row_blocks.append([])

            for x in range(0, self.size_x):
                if(self.matrix[y][x] == 0):
                    n_free += 1

                    if(x == self.size_x - 1 and n_free >= min_block_size):
                        self.row_blocks[y].append((x - n_free + 1, x))
                else:
                    if(n_free < min_block_size):
                        n_free = 0
                        continue
                    
                    self.row_blocks[y].append((x - n_free, x - 1))
                    n_free = 0
                    
