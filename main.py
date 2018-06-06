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
presents = presents[::-1]

# Creating a Sleigh of 1000x1000
sleigh = Sleigh(1000)

# Iterating over the presents list
with tqdm(total = len(presents)) as pbar:
    for present in presents:
        sleigh.fit_present(present)
        pbar.update(1)

# Writing the output file
with open(OUTPUT_FILE, "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for present in presents:
        writer.writerow(present.generate_output_list())