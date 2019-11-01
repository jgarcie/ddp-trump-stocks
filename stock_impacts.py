import csv
from datetime import datetime
from datetime import timedelta

# test variables
tweet_times = []
impact_time = 1 # in hours
trade_impact = 1 # in percentage 
stock_name = 'AAPL'

# global variables
trade_changes = []

# read tweet datetimes from txt
f = open("tweet_times.txt", "r")
for x in f:
    tweet_times.append(datetime.strptime(x.strip(), '%m/%d/%y %I:%M:%S %p'))
f.close()

# begin running through tweet datetimes
for tt in tweet_times:
    csv_name = './data/EQY_US_ALL_TRADE_' + str(tt.year) + str(tt.month).zfill(2) + str(tt.day).zfill(2)
    trade_before = {}
    trade_before_found = False
    trade_after = {}
    trade_after_found = False

    # open CSV and set up utility variables
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        impact_datetime = tt + timedelta(hours = impact_time)

        # begin reading CSV lines
        for row in csv_reader:
            if row[2] == stock_name:
                    curr_line_time = datetime.strptime(str(tt.year) + str(tt.month) + str(tt.day) + row[0][:6]\
                    , '%Y%m%d%H%M%S')

                    if trade_before_found is False:
                        if curr_line_time >= tt:
                            trade_before_found = True
                            if 'time' not in trade_before:
                                trade_before["time"] = curr_line_time
                                trade_before["price"] = row[5]
                        else:
                            trade_before["time"] = curr_line_time
                            trade_before["price"] = row[5]
                    elif trade_after_found is False:
                        if curr_line_time > impact_datetime: 
                            # IMPROVE: This should actually check for the closest possible time to impact_datetime
                            # instead of just defaulting to the previous trade_after line
                            trade_after_found = True
                            if 'time' not in trade_after:
                                trade_after["time"] = curr_line_time
                                trade_after["price"] = row[5]
                            break
                        else:
                            trade_after["time"] = curr_line_time
                            trade_after["price"] = row[5]

        # calculate stock price difference
        price_diff = (float(trade_after["price"]) - float(trade_before["price"])) / float(trade_before["price"])
        trade_changes.append(price_diff * 100)

# check for tweet impacts per timestamp
for i, tt in enumerate(tweet_times):
    impacted = False
    if abs(trade_changes[i]) > trade_impact:
        impacted = True
    print("TWEET:", tt, "IMPACTED:", impacted)