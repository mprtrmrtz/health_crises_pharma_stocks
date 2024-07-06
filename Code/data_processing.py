#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 14:21:54 2024

@author: mortezamaleki
"""

import os
import yfinance as yf
import pandas as pd
import warnings



os.getcwd()


# Suppress all warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)


# =============================================================================
# Pharma Stocks
# =============================================================================


# List of health and pharma sector companies' ticker symbols
tickers = ['JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'GILD', 'LLY', 'GSK', 'NVO', 'AMGN', 'AZN','BMY', 'CVS', 'GSK', 'MRNA', 'REGN', 'SNY', 'VRTX', 'BIIB']

# Fetch historical data for all tickers
data = {}
for ticker in tickers:
    data[ticker] = yf.download(ticker, start='2000-01-01', end='2023-12-31')

# Convert to a single DataFrame with multi-index columns
stock_data = pd.concat(data, axis=1)

# Flatten the multi-index columns

stock_data_raw = stock_data.copy()
stock_data_raw.columns = ['_'.join(col).strip() for col in stock_data_raw.columns.values]


stock_data_raw.to_csv('Code & Data/Health Sector/stock_data_raw.csv')

# List of stock-related variables
stock_variables = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

# Compute the aggregated values
aggregated_stock_data = pd.DataFrame()

for var in stock_variables:
    # Calculate the mean for each date across all tickers
    aggregated_stock_data[f'{var}_mean'] = stock_data.xs(var, level=1, axis=1).mean(axis=1)
    # Calculate the sum for volume
    if var == 'Volume':
        aggregated_stock_data[f'{var}_sum'] = stock_data.xs(var, level=1, axis=1).sum(axis=1)


# =============================================================================
# Macroeconomic Data
# =============================================================================

from fredapi import Fred
import pandas as pd

# Replace with your FRED API key
fred = Fred(api_key='<API Key>')

# Define the series and their corresponding FRED codes
series_codes = {
    'GDP': 'GDP',
    'Inflation': 'CPIAUCSL',
    'Unemployment_Rate': 'UNRATE',
    'Federal_Funds_Rate': 'FEDFUNDS',
    'Consumer_Sentiment_Index': 'UMCSENT',
    'Industrial_Production_Index': 'INDPRO',
    'M2_Money_Stock': 'M2',
    'Mortgage_Rate_30Y_Fixed': 'MORTGAGE30US',
    'Treasury_Rate_10Y': 'GS10',
    'Nonfarm_Payroll_Employment': 'PAYEMS',
    'Housing_Starts': 'HOUST',
    'Retail_Sales': 'RSAFS',
    'Personal_Consumption_Expenditures': 'PCE',
    'Producer_Price_Index': 'PPIACO',
    'Trade_Balance': 'BOPGTB',
    'Corporate_Profits': 'CP',
    'Government_Debt': 'GFDEBTN',
    'Exchange_Rate_USD_EUR': 'DEXUSEU',
    'Gross_Private_Domestic_Investment': 'GPDI',
    'Personal_Savings_Rate': 'PSAVERT',
    'Consumer_Credit': 'TOTALSL',
    'Real_Disposable_Personal_Income': 'DSPIC96',
    'Capacity_Utilization': 'TCU',
    'Inflation_Expectations': 'T10YIE'
}

# Fetch the data and store in a dictionary
data_dict = {}
for name, code in series_codes.items():
    # print(name)
    data_dict[name] = fred.get_series(code, start='2000-01-01', end='2024-12-31')

# Convert the dictionary to a DataFrame
macro_data_master = pd.DataFrame(data_dict)


macro_data = macro_data_master.copy()

macro_data['date'] = macro_data.index

# Resample the data to daily frequency and forward fill missing values
# Resample the data to daily frequency
macro_data = macro_data.resample('D').mean()

# Forward fill missing values
macro_data = macro_data.ffill()

# Filter the data from the beginning of 2000 to the end of 2023
macro_data = macro_data[(macro_data['date'] >= '2000-01-01') & (macro_data['date'] <= '2023-12-31')]



# =============================================================================
# Market Data
# =============================================================================

# Define the market indices you want to add
market_indices = {
    'SP500': '^GSPC',  # S&P 500
    'NASDAQ': '^IXIC'  # NASDAQ Composite
}

# Fetch historical data for market indices
market_data = {}
for market_name, ticker in market_indices.items():
    market_data[market_name] = yf.download(ticker, start='2000-01-01', end='2023-12-31')['Close']

# Convert to DataFrame
market_data_df = pd.DataFrame(market_data)

# Ensure the date column is the market and in datetime format
market_data_df.index = pd.to_datetime(market_data_df.index)



# =============================================================================
# Merged Data
# =============================================================================

stock_data = aggregated_stock_data.copy()

stock_data.index = pd.to_datetime(stock_data.index)

# Ensure the stock data is filtered from the beginning of 2000 to the end of 2023
stock_data = stock_data[(stock_data.index >= '2000-01-01') & (stock_data.index <= '2023-12-31')]

merged_data = stock_data.merge(macro_data, left_index=True, right_index=True, how='left')

merged_data = merged_data.merge(market_data_df, left_index=True, right_index=True, how='left')

# Column naming dictionary
variable_mapping = {
    'Open_mean': 'ST-OM', 'High_mean': 'ST-HM', 'Low_mean': 'ST-LM', 'Close_mean': 'ST-CM',
    'Adj Close_mean': 'ST-AM', 'Volume_mean': 'ST-VM', 'Volume_sum': 'ST-VS',
    'GDP': 'MA-GP', 'Inflation': 'MA-IF', 'Unemployment_Rate': 'MA-UR', 'Federal_Funds_Rate': 'MA-FF',
    'Consumer_Sentiment_Index': 'MA-CS', 'Industrial_Production_Index': 'MA-IP', 'M2_Money_Stock': 'MA-M2',
    'Mortgage_Rate_30Y_Fixed': 'MA-MR', 'Treasury_Rate_10Y': 'MA-TR', 'Nonfarm_Payroll_Employment': 'MA-NP',
    'Housing_Starts': 'MA-HS', 'Retail_Sales': 'MA-RS', 'Personal_Consumption_Expenditures': 'MA-PC',
    'Producer_Price_Index': 'MA-PP', 'Trade_Balance': 'MA-TB', 'Corporate_Profits': 'MA-CP', 'Government_Debt': 'MA-GD',
    'Exchange_Rate_USD_EUR': 'MA-ER', 'Gross_Private_Domestic_Investment': 'MA-GI', 'Personal_Savings_Rate': 'MA-PS',
    'Consumer_Credit': 'MA-CC', 'Real_Disposable_Personal_Income': 'MA-RI', 'Capacity_Utilization': 'MA-CU',
    'Inflation_Expectations': 'MA-IE', 'date': 'DT-DT', 'SP500': 'MI-SP', 'NASDAQ': 'MI-NS'
}


merged_data.rename(columns=variable_mapping, inplace=True)

merged_data.to_csv('Code & Data/Health Sector/aggregated_data.csv')










































