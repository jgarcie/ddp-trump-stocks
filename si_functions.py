import os.path
import csv
from datetime import datetime
from datetime import timedelta

def test_date_validity(test_date, file_loc, file_prefix):
    filepath = file_loc + file_prefix + str(test_date.year) + str(test_date.month).zfill(2) + str(test_date.day).zfill(2)
    if os.path.isfile(filepath):
        return True
    else:
        return False 

def get_next_valid_date(test_date, file_loc, file_prefix):
    valid_date = False

    test_date += timedelta(days=1)

    while valid_date is False:
        filepath = file_loc + file_prefix + str(test_date.year) + str(test_date.month).zfill(2) + str(test_date.day).zfill(2)
        if os.path.isfile(filepath):
            valid_date = test_date
        else:
            test_date += timedelta(days=1)

    return valid_date

def get_prev_valid_date(test_date, file_loc, file_prefix):
    valid_date = False

    while valid_date is False:
        filepath = file_loc + file_prefix + str(test_date.year) + str(test_date.month).zfill(2) + str(test_date.day).zfill(2)
        if os.path.isfile(filepath):
            valid_date = test_date
        else:
            test_date -= timedelta(days=1)

    return valid_date

def get_trade_times_and_values(d, impact_time, stock_name, csv_name, trade_before, trade_after, trade_data):
    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')
        impact_datetime = d + timedelta(hours = impact_time)

        # begin reading CSV lines
        for row in csv_reader:
            if row[2] == stock_name:
                    curr_line_time = datetime.strptime(str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2) \
                    + row[0][:6], '%Y%m%d%H%M%S')

                    if trade_data["before"] is False:
                        if curr_line_time >= d:
                            trade_data["before"] = True    
                            if 'time' not in trade_before:
                                trade_before["time"] = curr_line_time
                                trade_before["price"] = row[5]
                        else:
                            trade_before["time"] = curr_line_time
                            trade_before["price"] = row[5]
                    elif trade_data["after"] is False:
                        if curr_line_time > impact_datetime: 
                            # IMPROVE: This should actually check for the closest possible time to impact_datetime
                            # instead of just defaulting to the previous trade_after line
                            trade_data["after"] = True
                            if 'time' not in trade_after:
                                trade_after["time"] = curr_line_time
                                trade_after["price"] = row[5]
                            break
                        else:
                            trade_after["time"] = curr_line_time
                            trade_after["price"] = row[5]
    return

def get_outofbounds_trade_before(d, stock_name, file_loc, file_prefix, trade_before):
    d -= timedelta(days=1)
    d = get_prev_valid_date(d, file_loc, file_prefix)
    csv_name = file_loc + file_prefix + str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)

    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for row in csv_reader:
            if row[2] == stock_name:
                trade_before["time"] = datetime.strptime(str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2) \
                + row[0][:6], '%Y%m%d%H%M%S')
                trade_before["price"] = row[5]
            elif 'time' in trade_before:
                break
    return

def get_outofbounds_trade_after(d, stock_name, file_loc, file_prefix, trade_after):
    d = get_next_valid_date(d, file_loc, file_prefix)
    csv_name = file_loc + file_prefix + str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)

    with open(csv_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|')

        for row in csv_reader:
            if row[2] == stock_name:
                trade_after["time"] = datetime.strptime(str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2) \
                + row[0][:6], '%Y%m%d%H%M%S')
                trade_after["price"] = row[5]
                break
    return
