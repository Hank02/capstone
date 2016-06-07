import urllib.request
import time
import random
import csv
import datetime
import calendar

def update_db(ticker_list):
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
        # remove last element which contains last trading day in DB
        splitdata.pop()
        
        # create and open outfile
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
    

ticker_list = ["BMV:AC", "BMV:FHIPO14", "BMV:AEROMEX"]
update_db(ticker_list)