from numpy import savetxt
from tqdm import tqdm
from itertools import islice

from src.sleigh import Sleigh 

class Elf:
    def __init__(self, presents, matrix_size = 1000, from_x = 0, from_y = 0):
        # Presents sublist
        self.presents = presents
        self.num_presents = len(self.presents)

        # Submatrix size and starting points
        self.size = matrix_size
        self.from_x = from_x
        self.from_y = from_y

        # Creating a Sleigh
        self.sleigh = Sleigh(self.size)

    def start_working(self):
        # Fitted presents list
        fitted = 0

        # Should the matrix rotate?
        rotate_matrix = False

        # This is the main cycle.
        # It manages the package iteration and
        # when the Sleight class has to change
        # his level.
        with tqdm(total = self.num_presents) as pbar:
            while fitted < self.num_presents:
                # Check if at least an insertion has happened
                has_changed = False

                for pid, present in enumerate(self.presents):
                    if(present.point != False):
                        continue

                    fitted_point = self.sleigh.fit_present(present, rotate_matrix = rotate_matrix)

                    if(fitted_point != False):
                        # Update progress
                        pbar.update(1)
                        fitted += 1
                        has_changed = True

                        # Check if it's time to change level
                        if(self.sleigh.is_time_to_change()):
                            self.sleigh.next_operable_level()
                            self.sleigh.recompute_blocks()
                            rotate_matrix = False

                        # Check if it's time to rotate
                        if(rotate_matrix == False and fitted_point[1] >= (self.sleigh.size / 2) + 1):
                            rotate_matrix = True

                # If no presents fitted during
                # this last cycle, then it's time
                # to change level
                if(has_changed == False):
                    self.sleigh.next_operable_level()
                    self.sleigh.recompute_blocks()
                    rotate_matrix = False

        # Return fitted presents
        return self.presents
