import sys
import urllib.request
import time
import random

def get_ticker_list():
# takes csv file and retrieves list of tickers into list

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


def get_historic(ticker):
# receives a ticker and outputs timer series with date and close
    
    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate=Jan+01%2C+2016&output=csv"
    
    # add ticker to URL
    url = chunk1 + ticker + chunk2
    
    # open URL as "response" and read it into "data"
    with urllib.request.urlopen(url) as response:
        # read url object and store as string
        rawdata = response.read().decode('utf-8')

    # split string into continuous list (D, O, H, L, C, V)
    splitdata = rawdata.split('\n')
    
    # remove last element which is always empty
    splitdata.pop()
    
    # create list to store target data and add column headers
    outdata = [["Date", ticker]]
    
    # iterate over list...
    for index, each in enumerate(splitdata):
        # split each element into list
        splitter = each.split(',')
        # reset temporary list
        temp = []
        # skip firs element with column headers
        if index != 0:
            # append date [0] and close [4] "fields"
            temp.append(ticker)
            temp.append(splitter[0])
            temp.append(float(splitter[4]))
            # append date/close to outdata as a list of two elements
            outdata.append(temp)
    
    return outdata