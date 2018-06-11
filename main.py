import csv
from numpy import savetxt
from tqdm import tqdm
from itertools import islice

from src.elf import Elf
from src.present import Present

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

# Create and execute an elf
elf1 = Elf(presents)
res_presents = elf1.start_working()

# Writing the output file
with open(OUTPUT_FILE, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for present in res_presents:
        writer.writerow(present.generate_output_list())

# savetxt('matrix.out', sleigh.matrix, fmt = "%i", delimiter = "\t")