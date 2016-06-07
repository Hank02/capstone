import sys
import csv

# open file in read mode
datafile = open(sys.argv[1], "r")
# create reader object using csv lib
reader = csv.reader(datafile)

# open target file
targetfile = open("price_db.csv", "w")
# create writer object using csv lib
writer = csv.writer(targetfile, delimiter = ',')

# select date & close price columns from datafile and write to target
for row in reader:
    temp = []
    data = []
    temp.append(row[0])
    temp.append(row[4])
    data.append(temp)
    writer.writerows(data)

# close both files
datafile.close()
targetfile.close()
