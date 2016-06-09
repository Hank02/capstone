import sys
import urllib.request
import time
import random
import csv
import datetime
import calendar
import requests


def get_ticker_list():
# takes in csv file with tickers in Google Finance format
# and stores them in list

    # open csv file, quit if not found
    try:
        datafile = open(sys.argv[2], "r")
    except OSError as err:
        print("There was a roblem with the file")
        print("OS Error: {}".format(err))
        return 99
    
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

def validate_tickers(ticker):
# buils string with url
# calls API and makes sure response 200 is returned
# if not, print message and continue
    
    # wait for next call to avoid being blocked by Google
    #time.sleep(random.randint(2, 4))
    
    url_chunk = "http://www.google.com/finance/info?client=ig&q="
    
    # add ticker to URL
    url = url_chunk + ticker
    
    # call API and chech response
    response = requests.get(url)
    if response.status_code != 200:
        print("{} returns an error...".format(ticker))
        return 1
    else:
        return 0

def call_API(chunk1, chunk2, ticker):
# buils string with url
# calls API, decodes bits, splits by newlines
# returns a list of lists
# each list within list contains D, O, H, L, C, V
    
    # wait for next call to avoid being blocked by Google
    time.sleep(random.randint(2, 10))
    
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
    return splitdata

def store_date_and_price(ticker, splitdata, outdata):
# used for first ticker in ticker_list
# stores date and closing price for said ticker
# returns list of lists (with date and price) and number of days
    
    # store column headers
    outdata = [["Date", ticker]]
    
    # keep track of trade days in first ticker only
    trade_days = 0
    
    # iterate over list...
    for index, each in enumerate(splitdata):
        # skip firs element with column headers
        if index != 0:
            # split each element into list
            splitter = each.split(',')
            # reset temporary list
            temp = []

            # append date [0] and close [4] "fields"
            temp.append(splitter[0])
            temp.append(float(splitter[4]))
            
            # append date/close to outdata as a list of two elements
            outdata.append(temp)
            trade_days = index
    
    # print messge and return
    print("Done with {}".format(ticker))
    return outdata, trade_days

def store_price_only(ticker, splitdata, outdata, trade_days):
# used for all non-first tickers in ticker_list
# stores date and closing price for said ticker
# returns list of lists (with date and price) and number of days
    
    # store ticker as column header
    outdata[0].append(ticker)
    
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
    
    # if series is shorter than first, fill remaining spaces with 0s
    if control < trade_days:
        for index in range(trade_days - control):
            control += 1
            outdata[control].append(float(0))
    
    # print message and return
    print("Done with {}".format(ticker))
    return outdata

def reverse_order_of_tiemseries(outdata):
# takes list of lists with price data where oldest prices are at bottom
# crates new list, adds headers at top
# then reverses order of price data, newest prices at bottom

    # create new list to store data correctly (oldest data first)
    correctdata = []
    
    # first insert headers at top
    correctdata.append(outdata[0])
    
    # then add oldest data (at end of outdata) to top of correctdata
    for each in outdata[::-1]:
        correctdata.append(each)
    
    # remove headers writen at bottom of correctdata
    correctdata.pop()
    
    # print message and return
    print("Done swaping order of prices...")
    return correctdata

def write_to_csv_file(correctdata):
# creates new csv
# stores ordered data
    # create and open outfile
    outfile = open("histirical_prices.csv", "a")
    # create writer object
    writer = csv.writer(outfile)
    # write data in correctdata into csv file and close
    writer.writerows(correctdata)
    outfile.close()

def check_if_csv_uptodate():
# opens csv with existing data and reads it
# first column of file must contain date
# latest prices must be at bottom of file
    
    # open existing csv file, quit if not found
    try:
        data_file = open("histirical_prices.csv", "r")
    except OSError as err:
        print("There was a roblem with the file")
        print("OS Error: {}".format(err))
        return 99, 99, 99
    
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
        return 0, 0, 0
    else:
        print("File is not up-to-date... updating now...")
        return day, month, year



#################################################################################



def ticker_list_validation():
# makes sure all tickers in list are correct
    
    # check if right number of CL arguments provided
    arguments = len(sys.argv)
    if arguments != 3:
        print("Please enter path to csv file containing ticker list")
        return
    
    # populate list with stocks to retrieve
    tlist = get_ticker_list()
    if tlist == 99:
        return
    
    # check for response errors
    errors = 0
    for each in tlist:
        errors += validate_tickers(each)
    
    print("There were {} errors".format(errors))

def initial_APIcall():
# used to first populate db into csv
# takes one command-line argument: path to csv with target tickers

    # check if right number of CL arguments provided
    arguments = len(sys.argv)
    if arguments != 3:
        print("Please enter path to csv file containing ticker list")
        return
    
    # populate list with stocks to retrieve
    tlist = get_ticker_list()
    if tlist == 99:
        return
    
    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate=Jul+01%2C+2014&output=csv"
    
    # create list to hold data
    outdata = []
    
    # iterate over each ticker...
    for index, ticker in enumerate(tlist):
        # call API and get data
        splitdata = call_API(chunk1, chunk2, ticker)
        # on first ticker only...
        if index == 0:
            # store a date columen before the price column
            outdata, days = store_date_and_price(ticker, splitdata, outdata)
        # for all other tickers in list...
        else:
            # only store price column
            outdata = store_price_only(ticker, splitdata, outdata, days)
    
    # reverse order of prices: latest at bottom
    correctdata = reverse_order_of_tiemseries(outdata)
    
    # write data to csv file
    write_to_csv_file(correctdata)


def update_csv_file():
# used to update existing csv file
# quits if file not found
    # check if right number of CL arguments provided
    arguments = len(sys.argv)
    if arguments != 3:
        print("Please enter path to csv file containing ticker list")
        return

    # populate list with stocks to retrieve
    tlist = get_ticker_list()
    if tlist == 99:
        return

    # get last date in csv file
    day, month, year = check_if_csv_uptodate()
    # if up to date (0) or file not found (99), exit
    if day == 0 or day == 99:
        return
    
    # build URL from Google Finance API
    chunk1 = "http://www.google.com/finance/historical?q="
    chunk2 = "&startdate="+month+"+"+day+"%2C"+"+"+year+"&output=csv"
    
    # create list to hold data
    outdata = []
    
    # iterate over each ticker...
    for index, ticker in enumerate(tlist):
        # call API and get data
        splitdata = call_API(chunk1, chunk2, ticker)
        # on first ticker only...
        if index == 0:
            # store a date columen before the price column
            outdata, days = store_date_and_price(ticker, splitdata, outdata)
        # for all other tickers in list...
        else:
            # only store price column
            outdata = store_price_only(ticker, splitdata, outdata, days)
    
    # reverse order of prices: latest at bottom
    correctdata = reverse_order_of_tiemseries(outdata)
    
    # write data to csv file
    write_to_csv_file(correctdata)



#################################################################################

if __name__ == '__main__':
    if sys.argv[1] == "initial_APIcall":
        initial_APIcall()
    elif sys.argv[1] == "update_csv_file":
        update_csv_file()
    elif sys.argv[1] == "ticker_list_validation":
        ticker_list_validation()