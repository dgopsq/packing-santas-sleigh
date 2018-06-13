import csv
from numpy import savetxt
from tqdm import tqdm
from itertools import islice

from src.present import Present
from src.sleigh import Sleigh

# Options
PRESENTS_DATASET = "./dataset/presents_small.csv"
OUTPUT_FILE = "./solution.out"

# List of Present objects
presents = []

# Reading the presents
with open(PRESENTS_DATASET) as f:
    reader = csv.reader(f)
    next(reader)
    presents = [Present(*r) for r in reader]

# Initialize Sleigh
sleigh = Sleigh(1000, 1000)

# Start fitting
with tqdm(total = len(presents)) as pbar:
    for present in presents:
        fitted_point = sleigh.fit_present(present)

        # Update status
        pbar.update(1)

        # Update present's point
        present.set_point(fitted_point)

last_present = sorted(presents, key = lambda p: p.point[2] + p.z, reverse = True)[0]
max_value = last_present.point[2] + last_present.z

# Writing the output file
with open(OUTPUT_FILE, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')

    # Header
    writer.writerow(['PresentId', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'x4', 'y4', 'z4', 'x5', 'y5', 'z5', 'x6', 'y6', 'z6', 'x7', 'y7', 'z7', 'x8', 'y8', 'z8'])

    # Rows
    for present in presents:
        writer.writerow(present.generate_output_list(max_value))