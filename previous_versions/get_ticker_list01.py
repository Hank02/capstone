import sys
import csv

# open file in read mode
datafile = open(sys.argv[1], "r")
# create reader object using csv lib
reader = csv.reader(datafile)

# store contents into list
ticker_list = []
for row in reader:
    ticker_list.append(row[0])

# close csv file
datafile.close()

# print list for confirmation
print(ticker_list)
print(len(ticker_list))

# still need to add these to tickers_db