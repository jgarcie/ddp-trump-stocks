import csv
from datetime import datetime
from datetime import timedelta

from si_functions import *

# default variables
impact_time = 1 # in hours
trade_impact = 1 # in percentage 
stock_name = 'AMZN'
file_loc = '/Volumes/Seagate Expansion Drive/Stocks Data'
file_prefix = '/EQY_US_ALL_TRADE_'
results_file = './results.txt'

# global variables
tweet_times = []
trades = []
trade_changes = []
tweet_counter = 1

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
        trades.append({"tb_time": trade_before["time"], "tb_price": trade_before["price"], \
        "ta_time": trade_after["time"], "ta_price": trade_after["price"]})
        price_diff = (float(trade_after["price"]) - float(trade_before["price"])) / float(trade_before["price"])
        trade_changes.append(price_diff * 100)
    else:
        trades.append(False)
        trade_changes.append(False)
    
    print(str(tweet_counter) + "/" + str(tweet_total))
    tweet_counter += 1

# check for tweet impacts per timestamp and write to results file
res = open(results_file, "w+")
for i, tt in enumerate(tweet_times):
    tt_adjusted = tt - timedelta(hours=5) # GMT to EST adjustment
    impacted = False
    if trade_changes[i] is False:
        impacted = 'N/A'
    elif abs(trade_changes[i]) > trade_impact:
        impacted = True
    
    if trades[i] is not False:
        res.write("TWEET TIME: " + tt_adjusted.strftime('%m/%d/%Y %I:%M:%S %p') + " IMPACTED: " + str(impacted) \
        + " CHANGE: " + str(round(trade_changes[i], 3)) + "% (FROM: " + trades[i]["tb_time"].strftime('%m/%d/%Y %H:%M:%S') \
        + " - $" + trades[i]["tb_price"] + "; TO: " + trades[i]["ta_time"].strftime('%m/%d/%Y %H:%M:%S') \
        + " - $" + trades[i]["ta_price"] + ")" + '\n')
    else:
        res.write("TWEET TIME: " + tt_adjusted.strftime('%m/%d/%Y %I:%M:%S %p') + " IMPACTED: " + str(impacted) + '\n')

res.close()
print('Finished!')