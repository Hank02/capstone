import urllib.request
import time
import random
import csv

# saves hispotical prices into csv
# function takes list of tickers as input
# places 0 where no data is available
# first ticker in list MUST be the one with the longest series
# places newest data at bottom

def get_historic(ticker_list):
# receives a list of tickers and outputs time series with date and close
    
    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate=Jul+01%2C+2014&output=csv"
    
    # create and open outfile
    outfile = open("histirical_prices.csv", "a")
    # create writer object
    writer = csv.writer(outfile)

    # iterate over list and call Google Finance API
    for indx, ticker in enumerate(ticker_list):
        # wait for next call to avoid being blocked by Google (not before first call)
        time.sleep(random.randint(1, 10))
            
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
    
        # store column headers
        if indx == 0:
            outdata = [["Date", ticker]]
            # keep track of trade days in first ticker only
            trade_days = 0
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
                    trade_days = index
        else:
            # store ticker as column header
            outdata[0].append(ticker)
            # determine length of series less 1 (header)
            length = len(splitdata) - 1
            # iterate over time series
            control = 0
            for index, each in enumerate(splitdata):
                # split each element into list
                splitter = each.split(',')
                # skip firs element with column headers
                if index != 0:
                    # append price to outdata
                    outdata[index].append(float(splitter[4]))
                    control += 1
            if control < trade_days:
                    for index in range(trade_days - control):
                        control += 1
                        outdata[control].append(float(0))
            
        print("Done with {}".format(ticker))

    # create new list to store data correctly (oldest data first)
    correctdata = []
    # first add headers
    correctdata.append(outdata[0])
    # then add oldest data (at end of outdata) to top of correctdada
    for each in outdata[::-1]:
        correctdata.append(each)
    correctdata.pop()
    
    # write date/close to outfile as a list of two elements
    writer.writerows(correctdata)
    outfile.close()



ticker_list = ["BMV:AC", "BMV:FHIPO14", "BMV:AEROMEX"]

get_historic(ticker_list)




