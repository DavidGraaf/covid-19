import pandas as pd
from datetime import date
from datetime import timedelta
import numpy as np
import os.path
from os import path

#reading in the CSVs
hist_US_State = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv")
test_us_total_raw = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv", index_col='date')
test_us_total_raw = test_us_total_raw[test_us_total_raw["location"] == "United States"]
test_us_total_clean = test_us_total_raw.loc[:,["location", "total_cases", "new_cases",
                                               "total_tests", "new_tests", "positive_rate"]]

#Getting yesterday's date and the day before, this is for use later
today = date.today()
yesterday1 = today - timedelta(days = 1)
yesterday = str(yesterday1)
day_before_yesterday = today - timedelta(days = 2)
day_before_yesterday = str(day_before_yesterday)

#Creating the CSV for the test data up until and including yesterday's data
test_us_total_clean.loc[:yesterday].to_csv(r"C:\Users\david\OneDrive\Tableau\COVID-19\test_us_total_clean.csv")

#Creating two data frames: yesterday cases and the day before
yesterday_cases = hist_US_State[hist_US_State["date"] == yesterday]
day_before_yesterday_cases = hist_US_State[hist_US_State["date"] == day_before_yesterday]

#Create an empty dataframe and yesterday's cases to it
total_cases = pd.DataFrame()
total_cases = total_cases.append(yesterday_cases)

#Extracting the total cases from both dataframes to calculate the new number of cases and add them to a column
cases_list_1 = yesterday_cases['cases'].to_numpy()
cases_list_2 = day_before_yesterday_cases['cases'].to_numpy()
cases_list_3 = cases_list_1 - cases_list_2
total_cases["new_cases"] = cases_list_3

#Extracting the total deaths from both dataframes to calculate the new number of deaths and add them to a column
deaths_list_1 = yesterday_cases['deaths'].to_numpy()
deaths_list_2 = day_before_yesterday_cases['deaths'].to_numpy()
deaths_list_3 = deaths_list_1 - deaths_list_2
total_cases["new_deaths"] = deaths_list_3

#Check to see if the file already exists, if it does we perform another check to see if somehow yesterday's
#data was already appended, if this check is false (meaning: latest entry is day before yesterday), we append.
#if file does not exist yet, we create it.
if path.exists(r"C:\Users\david\OneDrive\Tableau\COVID-19\total_cases.csv"):
    with open(r"C:\Users\david\OneDrive\Tableau\COVID-19\total_cases.csv",'a') as f:
        check_DF = pd.read_csv(r"C:\Users\david\OneDrive\Tableau\COVID-19\total_cases.csv")
        check_str = check_DF.iloc[len(check_DF)-1,[1]].to_string()
        check_str = check_str[8:]
        if check_str == yesterday:
            pass
        else:
            total_cases.to_csv(f, header=False, line_terminator='\n')
else:
    total_cases.to_csv(r"C:\Users\david\OneDrive\Tableau\COVID-19\total_cases.csv")
