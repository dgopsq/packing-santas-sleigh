import csv
from numpy import savetxt
from tqdm import tqdm
from itertools import islice

from src.present import Present 
from src.sleigh import Sleigh 

# Options
PRESENTS_DATASET = "./dataset/presents.csv"
OUTPUT_FILE = "./solution.out"
SLEIGH_SIZE = 1000

# List of Present objects
presents = []

# Reading the presents
with open(PRESENTS_DATASET) as f:
    reader = csv.reader(f)
    next(reader)
    presents = [Present(*r) for r in reader]

# Reverse the presents
presents = presents[::-1][0:3000]

# Creating a Sleigh of 1000x1000
sleigh = Sleigh(1000)

# This is the main cycle.
# It manages the package iteration and
# when the Sleight class has to change
# his level.

# Fitted presents list
fitted = 0

# Should the matrix rotate?
rotate_matrix = False

num_presents = len(presents)

with tqdm(total = num_presents) as pbar:
    while fitted < num_presents:
        # Check if at least an insertion has happened
        has_changed = False

        for pid, present in enumerate(presents):
            if(present.point != False):
                continue

            fitted_point = sleigh.fit_present(present, rotate_matrix = rotate_matrix)

            if(fitted_point != False):
                # Update progress
                pbar.update(1)
                fitted += 1
                has_changed = True

                # Check if it's time to change level
                if(sleigh.is_time_to_change()):
                    sleigh.next_operable_level()
                    sleigh.recompute_blocks()
                    rotate_matrix = False
                    # print("To level {0}".format(sleigh.level))

                # Check if it's time to rotate
                if(rotate_matrix == False and fitted_point[1] >= (sleigh.size / 2) + 1):
                    rotate_matrix = True
                    # print("Rotate!")

        # If no presents fitted during
        # this last cycle, then it's time
        # to change level
        if(has_changed == False):
            sleigh.next_operable_level()
            sleigh.recompute_blocks()
            rotate_matrix = False
                
# Writing the output file
with open(OUTPUT_FILE, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for present in presents:
        writer.writerow(present.generate_output_list())

# savetxt('matrix.out', sleigh.matrix, fmt = "%i", delimiter = "\t")