import urllib.request
import csv
import time

ticker_list = ["BMV:AC"]

# build URL from Google Finance API
chunk1 = "http://www.google.com/finance/historical?q="
chunk2 = "&startdate=Jan+01%2C+2016&output=csv"

# iterate over list and call Google Finance API
isfirst = True
for ticker in ticker_list:
    # wait for next call to avoid being blocked by Google (not before first call)
    if isfirst:
        delay = 0
        isfirst = False
    else:
        delay = 4
    time.sleep(delay)
    
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
    
    # create list to store target data
    outdata = [["Date", "Close"]]
    # iterate over list...
    for index, each in enumerate(splitdata):
        # split each element into list
        splitter = each.split(',')
        # reset temporary list
        temp = []
        # skip firs element with column headers
        if index != 0:
            # append date [0] and close [4] "fields"
            temp.append(splitter[0])
            temp.append(float(splitter[4]))
            # append date/close to outdata as a list of two elements
            outdata.append(temp)
    print(outdata)



    