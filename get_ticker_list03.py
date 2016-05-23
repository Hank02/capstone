import sys

def get_ticker_list():
    # open file in read mode
    datafile = open(sys.argv[1], "r")
    
    # read file and split by newline
    reader = datafile.read().strip().split()
    
    # store contents into list
    ticker_list = []
    for row in reader:
        ticker_list.append(row)
    
    # close csv file and return
    datafile.close()
    return ticker_list

tlist = get_ticker_list()
print(tlist)
print(len(tlist))