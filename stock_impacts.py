import csv
from datetime import datetime
from datetime import timedelta

from si_functions import *

# default variables
impact_time = 1 # in hours
trade_impact = 1 # in percentage 
stock_name = 'BABA'
file_loc = '/Volumes/Seagate Expansion Drive/Stocks Data'
file_prefix = '/EQY_US_ALL_TRADE_'
results_file = './results.txt'

# global variables
tweet_times = []
tweet_counter = 1
res = open(results_file, "w+")

# read tweet datetimes from txt
f = open("tweet_times.txt", "r")
for x in f:
    tweet_times.append(datetime.strptime(x.strip(), '%m/%d/%Y %I:%M:%S %p'))
f.close()

tweet_total = len(tweet_times)

# begin running through tweet datetimes
for tt in tweet_times:
    tt_adjusted = tt - timedelta(hours=5) # GMT to EST adjustment
    trade_before = {}
    trade_after = {}
    trade_data = {"before": False, "after": False}

    if test_date_validity(tt_adjusted, file_loc, file_prefix):
        csv_name = file_loc + file_prefix + str(tt_adjusted.year) + str(tt_adjusted.month).zfill(2) + str(tt_adjusted.day).zfill(2)
        get_trade_times_and_values(tt_adjusted, impact_time, stock_name, csv_name, trade_before, trade_after, trade_data)
    else:
        get_outofbounds_trade_before(tt_adjusted, stock_name, file_loc, file_prefix, trade_before)
        trade_data["before"] = True
    
    if trade_data["before"] is False:
        get_outofbounds_trade_before(tt_adjusted, stock_name, file_loc, file_prefix, trade_before)
        trade_data["before"] = True
        get_trade_times_and_values(tt_adjusted, impact_time, stock_name, csv_name, trade_before, trade_after, trade_data)
    
    if trade_data["after"] is False:
        get_outofbounds_trade_after(tt_adjusted, stock_name, file_loc, file_prefix, trade_after)
        trade_data["after"] = True

    # calculate stock price difference and save for later
    if 'time' in trade_before and 'time' in trade_after:
        price_diff = (float(trade_after["price"]) - float(trade_before["price"])) / float(trade_before["price"])
        impacted = False
        if abs(price_diff * 100) > trade_impact:
            impacted = True

        res.write("TWEET TIME: " + tt_adjusted.strftime('%m/%d/%Y %I:%M:%S %p') + " IMPACTED: " + str(impacted) \
        + " CHANGE: " + str(round(price_diff * 100, 3)) + "% (FROM: " + trade_before["time"].strftime('%m/%d/%Y %H:%M:%S') \
        + " - $" + trade_before["price"] + "; TO: " + trade_after["time"].strftime('%m/%d/%Y %H:%M:%S') \
        + " - $" + trade_after["price"] + ")" + '\n')
    else:
        res.write("TWEET TIME: " + tt_adjusted.strftime('%m/%d/%Y %I:%M:%S %p') + " IMPACTED: False\n")
    
    print(str(tweet_counter) + "/" + str(tweet_total))
    tweet_counter += 1

res.close()
print('Finished!')