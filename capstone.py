import sys
import urllib.request
import time
import random
import csv
import datetime
import calendar



def get_ticker_list():
# takes in csv file with tickers in Google Finance format
# and stores them in list
    
    # open file in read mode
    datafile = open(sys.argv[2], "r")
    
    # read file and split by newline
    reader = datafile.read().strip().split()
    
    # store contents into list
    ticker_list = []
    for row in reader:
        ticker_list.append(row)
    
    # close csv file and return
    datafile.close()
    print("Ticker list contains {} stocks...".format(len(ticker_list)))
    return ticker_list




def get_historic(ticker_list):
# receives a list of tickers and outputs time series with date and close
# saves hispotical prices into csv
# function takes list of tickers as input
# places 0 where no data is available
# first ticker in list MUST be the one with the longest series
# places newest data at bottom
    
    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate=Jul+01%2C+2014&output=csv"
    
    # create and open outfile
    outfile = open("histirical_prices.csv", "a")
    # create writer object
    writer = csv.writer(outfile)

    # iterate over list and call Google Finance API
    for indx, ticker in enumerate(ticker_list):
        # wait for next call to avoid being blocked by Google
        time.sleep(random.randint(1, 20))
            
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




def update_db(ticker_list):
# takes in csv with historical price db
# checks latest date in db
# downloads prices from said date to last avalable
# references ticker_list
    
    
    # open existing csv file
    data_file = open("histirical_prices.csv", "r")
    
    # create reader object
    reader = csv.reader(data_file)
    
    # convert object into list
    reader = list(reader)
    
    # close file
    data_file.close()
    
    # store 0th element of list in last position
    last_date = reader[-1][0]
    print("Last trading day on file is {}".format(last_date))
    
    # split to make date easier to work with
    last_date = last_date.split("-")
    year = "20" + last_date[2]
    month = last_date[1]
    # add leading zero to day, if needed
    if len(last_date[0]) == 1:
        day = "0" + last_date[0]
    else:
        day = last_date[0]

    # check if file is up to date
    today = str(datetime.date.today())
    today = today.split("-")
    # convert month to numeric format
    today_month = calendar.month_abbr[int(today[1])]
    # compare today to last date on file
    if day == today[2] and month == today_month and year == today[0]:
        print("File is up-to-date!")
        return

    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate="+month+"+"+day+"%2C"+"+"+year+"&output=csv"
    
    # iterate over list and call Google Finance API
    for indx, ticker in enumerate(ticker_list):
        # wait for next call to avoid being blocked by Google
        time.sleep(random.randint(1, 20))
            
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
        # remove last element which contains last trading day in DB (repeated)
        splitdata.pop()
        
        # open outfile with existing db
        outfile = open("histirical_prices.csv", "a")
        # create writer object
        writer = csv.writer(outfile)
        
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
    # then add oldest data (at end of outdata) to top of correctdada
    for each in outdata[::-1]:
        correctdata.append(each)
    # remove last element which is always empty
    correctdata.pop()
    # remove headers (comment out this line to check ticker alignment)
    del correctdata[0]
    
    # write date/close to outfile as a list of two elements
    writer.writerows(correctdata)
    outfile.close()


def create_db():
    arguments = len(sys.argv)
    if arguments != 3:
        print("Please enter path to csv file containing ticker list")
        return
    
    tlist = get_ticker_list()
    get_historic(tlist)

def recent_prices():
    arguments = len(sys.argv)
    if arguments != 3:
        print("Please enter path to csv file containing ticker list")
        return
    
    tlist = get_ticker_list()
    update_db(tlist)

if __name__ == '__main__':
    if sys.argv[1] == "create_db":
        create_db()
    elif sys.argv[1] == "recent_prices":
        recent_prices()