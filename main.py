import csv
from numpy import savetxt
from tqdm import tqdm
from itertools import islice
from multiprocessing import Process, Queue

from src.elf import Elf
from src.present import Present
from src.sleigh import Sleigh 

# Options
PRESENTS_DATASET = "./dataset/presents.csv"
OUTPUT_FILE = "./solution.out"
SLEIGH_SIZE = 1000

# Create and execute an elf
def call_elf(res, elf_n, presents, sleigh, x, y):
    elf = Elf(elf_n, presents, sleigh, from_x = x, from_y = y)
    this_res_presents = elf.start_working()
    q.put(this_res_presents)

# Manage the main process
if __name__ == '__main__':
    # List of Present objects
    presents = []

    # Create a global presents array
    # for the result
    res_presents = []

    # Reading the presents
    with open(PRESENTS_DATASET) as f:
        reader = csv.reader(f)
        next(reader)
        presents = [Present(*r) for r in reader]

    # Reverse the presents
    presents = presents[::-1][0:3000]

    q = Queue(2)
    elf_team = []

    elf_team.append(Process(target = call_elf, args = (q, 1, presents[0:][::2], Sleigh(1000, 500), 0, 0)))
    elf_team.append(Process(target = call_elf, args = (q, 2, presents[1:][::2], Sleigh(1000, 500), 0, 500)))

    # Clear memory
    del presents

    for elf in elf_team:
        elf.start()

    # Get solutions
    res_presents = [q.get() for elf in elf_team]

    for elf in elf_team:
        elf.join()

    # Flatten solution
    res_presents = [item for sublist in res_presents for item in sublist]

    # Writing the output file
    with open(OUTPUT_FILE, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for present in res_presents:
            writer.writerow(present.generate_output_list())