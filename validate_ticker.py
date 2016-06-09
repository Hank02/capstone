import sys
import time
import random
import csv
import requests



def get_ticker_list():
# takes in csv file with tickers in Google Finance format
# and stores them in list

    # open csv file, quit if not found
    try:
        datafile = open(sys.argv[1], "r")
    except OSError as err:
        print("There was a roblem with the file")
        print("OS Error: {}".format(err))
        return 99
    
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
    
    # iterate over list and check response code
    response = requests.get(url)
    if response.status_code != 200:
        print("{} returns an error...".format(ticker))
    


tlist = get_ticker_list()
for each in tlist:
    validate_tickers(each)

