import csv
from numpy import savetxt

from src.present import Present 
from src.sleigh import Sleigh 

# List of Present objects
presents = []

# Reading the presents
with open("./dataset/presents.csv") as f:
    reader = csv.reader(f)
    next(reader)
    presents = [Present(*r) for r in reader]

# Reverse the presents
presents = presents[::-1]

# Debug 
presents = presents[0:100]

# Creating a Sleigh of 1000x1000
sleigh = Sleigh(1000)

# Iterating over the presents list
fitted = 0
for present in presents:
    if(sleigh.fit_present(present)):
        fitted += 1
        print("Fitted {0}".format(present.pid))

# Writing the output file
with open("solution.out", "w") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for present in presents:
        writer.writerow(present.generate_output_list())