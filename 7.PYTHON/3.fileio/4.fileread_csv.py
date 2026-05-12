import csv
filename = "data.csv"

data= []

with open(filename, "r", newline="") as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)

print(data)

data2 = []

with open(filename, "r", newline="") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data2.append(row)

print(data2)