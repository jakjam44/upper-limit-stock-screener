import time

import pandas as pd
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

'''
This function takes accesses a .csv sheet with columns = [Slno, Symbol, Company]
and generates the CMP of each company and saves it to another .csv file.
'''

# def GenerateCMPs(input_filename, output_filename):
#     df = pd.read_csv(input_filename)
#
#     start = dt.datetime(2021, 6, 3)
#     end = dt.datetime(2021, 6, 4)
#
#     for item in range(0, 1920):
#         try:
#             df.iloc[item, 3] = float((pdr.get_data_yahoo(df.iloc[item, 1], start, end).iloc[0, 3]))
#         except Exception:
#             df.iloc[item, 3] = None
#
#     obj = df.to_csv(output_filename)


def ClosePriceXDays(stock, num_days):
    list_prices = []
    list_dates = []

    list_dates.append(dt.date.today())

    i = 1

    while len(list_prices) <= num_days:
        list_dates.append(dt.date.today() - dt.timedelta(days=i))

        start = dt.datetime(list_dates[i - 1].year, list_dates[i - 1].month, list_dates[i - 1].day)
        end = dt.datetime(list_dates[i].year, list_dates[i].month, list_dates[i].day)

        try:
            price = float(pdr.get_data_yahoo(stock, end, start).iloc[0, 3])
            list_prices.append(round(price, 2))

        except Exception:
            pass

        i += 1

    return list_prices


def CalcPercentChange(list_prices):
    list_percent = []

    for j in range(0, num_days):
        percent = round((list_prices[j] - list_prices[j + 1]) * 100 / list_prices[j + 1], 2)
        list_percent.append(percent)

    return list_percent


def PercentCriteria(list_percent, criteria):
    counter = 0

    for k in range(0, num_days):
        if list_percent[k] >= criteria - 1 and list_percent[k] <= criteria + 1:
            counter += 1
        else:
            break

    if counter == num_days:
        return True
    else:
        return False


num_days = int(input("How many days' data do you want to anaylse?  "))

penst_lim = int(input("Below what price would you consider a stock a penny stock?  "))

percent_criteria = int(input("What percentage do you want to consider as Upper Limit?  "))

df = pd.read_csv("StockCMPs.csv")

list_of_prices = []
list_of_percents = []
list_of_stocks = []

t1 = time.perf_counter()

for item in range(0,1920):
    try:
        if df.iloc[item, 3] <= penst_lim:
            list_of_prices = ClosePriceXDays(df.iloc[item, 1], num_days)
            list_of_percents = CalcPercentChange(list_of_prices)
            Yes_or_No = PercentCriteria(list_of_percents, percent_criteria)
            if Yes_or_No is True:
                list_of_stocks.append(df.iloc[item, 1])
    except Exception:
        pass

t2 = time.perf_counter()

print("The stocks that qualify are:\n")
for item in list_of_stocks:
    print(f"{item}\n")

print(f"Finished in {t2-t1} seconds.")