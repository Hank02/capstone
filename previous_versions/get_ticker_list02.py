import sys
import csv

def get_ticker_list():
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
    return ticker_list

tlist = get_ticker_list()
print(tlist)
print(len(tlist))