import csv

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

# Creating a Sleigh of 1000x1000
sleigh = Sleigh(1000)

# Iterating over the presents list
fitted = 0
for present in presents:
    if(sleigh.fit_present(present)):
        fitted += 1
        print("Fitted {0}".format(present.pid))