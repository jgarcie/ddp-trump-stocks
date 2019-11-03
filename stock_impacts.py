import csv
from datetime import datetime
from datetime import timedelta

# default variables
impact_time = 1 # in hours
trade_impact = 1 # in percentage 
stock_name = 'BABA'
stock_loc = '/Volumes/Seagate Expansion Drive/Stocks Data'
stock_prefix = '/EQY_US_ALL_TRADE_'
results_file = './results.txt'

# global variables
tweet_times = []
trade_changes = []
tweet_counter = 1

# read tweet datetimes from txt
f = open("tweet_times.txt", "r")
for x in f:
    tweet_times.append(datetime.strptime(x.strip(), '%m/%d/%y %I:%M:%S %p'))
f.close()

tweet_total = len(tweet_times)

# begin running through tweet datetimes
for tt in tweet_times:
    csv_name = stock_loc + stock_prefix + str(tt.year) + str(tt.month).zfill(2) + str(tt.day).zfill(2)
    trade_before = {}
    trade_before_found = False
    trade_after = {}
    trade_after_found = False

    # open CSV and set up utility variables
    try:
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
    except FileNotFoundError:
        trade_changes.append(False)
    
    print(str(tweet_counter) + "/" + str(tweet_total))
    tweet_counter += 1

# check for tweet impacts per timestamp and write to results file
res = open(results_file, "w+")
for i, tt in enumerate(tweet_times):
    impacted = False
    if trade_changes[i] is False:
        impacted = 'N/A'
    elif abs(trade_changes[i]) > trade_impact:
        impacted = True
    res.write("TWEET TIME: " + tt.strftime('%m/%d/%y %I:%M:%S %p') + "; IMPACTED: " + str(impacted) + '\n')

res.close()
print('Finished!')