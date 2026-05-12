import csv

data =[[
    "Name", "Age", "City"],
    ["John", 25, "Seoul"],
    ["Jane", 30, "Busan"],
    ["Bob", 35, "Daegu"]
]

filename = "data.csv"

with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)


data2 =[
    {"Name":"John", "Age":22, "City":"Seoul"},
    {"Name":"Jane", "Age":21, "City":"Busan"},
    {"Name":"Bob", "Age":20, "City":"Daegu"}
]

with open(filename, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Name", "Age", "City"])
    writer.writeheader()
    writer.writerows(data2)