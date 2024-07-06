#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 14:27:12 2024

@author: mortezamaleki
"""

import pandas as pd

import warnings

import matplotlib.pyplot as plt
import sklearn
import seaborn as sns


aggregated_data = pd.read_csv('Code & Data/Health Sector/aggregated_data.csv')
stock_data_raw = pd.read_csv('Code & Data/Health Sector/stock_data_raw.csv')


# =============================================================================
#  Correlation Plot
# =============================================================================

correlation_matrix = aggregated_data.copy()
correlation_matrix.drop(columns = ['DT-DT', 'Date'], inplace = True)

# Compute the correlation matrix
correlation_matrix = correlation_matrix.corr()

sns.set(font_scale=1.2)
clustermap = sns.clustermap(
    correlation_matrix,
    fmt=".2f",
    cmap='coolwarm',
    vmin=-1,
    vmax=1,
    annot_kws={"size": 10},
    figsize=(15, 15)
)

# Add title and improve legend
clustermap.ax_heatmap.tick_params(axis='both', which='major', labelsize=12)

# Adjust the legend position
for text in clustermap.ax_heatmap.get_yticklabels():
    text.set_rotation(0)

plt.savefig("Figures/correlation_plot.pdf", dpi = 300)

plt.show()

# =============================================================================
# Time Series All
# =============================================================================

time_series_all = stock_data_raw.copy()

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned and processed stock data
# Ensure `stock_data_raw` is preprocessed and ready to use


# Define the tickers
tickers = ['JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'GILD', 'LLY', 'GSK', 'NVO', 'AMGN', 'AZN']

# Important health-related events
events = {
    '2001-09-01': 'Anthrax Attacks',
    '2003-03-01': 'SARS Outbreak',
    '2006-06-01': 'HPV Vaccine Approval',
    '2009-04-01': 'H1N1 Pandemic',
    '2012-09-01': 'MERS Outbreak',
    '2014-03-01': 'Ebola Outbreak',
    '2015-05-01': 'Zika Virus Outbreak',
    '2017-08-01': 'CAR-T Cell Therapy Approval',
    '2020-03-01': 'COVID-19 Pandemic',
    '2021-01-01': 'Mass Vaccination Campaigns',
    '2022-12-01': 'COVID-19 Variants'
}

# Ensure the index is in datetime format
time_series_all.index = pd.to_datetime(time_series_all.Date)

# Plot closing prices with events
plt.figure(figsize=(14, 6))
ax = plt.gca()

# Plot each ticker's closing prices
for ticker in tickers:
    if f'{ticker}_Close' in time_series_all.columns:
        plt.plot(time_series_all.index, time_series_all[f'{ticker}_Close'], label=ticker)

# Highlight events
for date, event in events.items():
    event_date = pd.to_datetime(date)
    if event_date >= time_series_all.index.min() and event_date <= time_series_all.index.max():
        plt.axvline(event_date, linestyle='--', alpha=0.6, label=event)

# Remove duplicate event labels in the legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
legend = plt.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1, 1))

# Set white background for plot and legend
ax.set_facecolor('white')
plt.gcf().set_facecolor('white')
frame = legend.get_frame()
frame.set_facecolor('white')
frame.set_edgecolor('black')

plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.tight_layout()

plt.savefig("Figures/all_timesereis_plot.pdf", dpi = 300)

plt.show()


# =============================================================================
# Distributions
# =============================================================================

# Load the data
data = aggregated_data.copy()

# Convert the date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Set the date column as the index
data.set_index('Date', inplace=True)

# Variables for histograms
variables = ['ST-CM', 'MA-GP', 'MA-IF', 'MI-SP', 'MI-NS', 'MA-UR']

# Set the style of the visualization
sns.set(style='whitegrid')

# Create histograms for the selected variables
plt.figure(figsize=(12, 6))

for i, var in enumerate(variables, 1):
    plt.subplot(2, 3, i)
    sns.histplot(data[var], kde=True, bins=30)
    plt.title(f'Distribution of {var}')
    plt.xlabel(var)
    plt.ylabel('Frequency')

plt.tight_layout()


plt.savefig('Figures/distributions.pdf', dpi = 300)

plt.show()



# =============================================================================
#   Box Plot
# =============================================================================

# Load the data
data = aggregated_data.copy()

# Convert the date column to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Set the date column as the index
data.set_index('Date', inplace=True)

# Define significant events with their start dates
events = {
    '2001-10-01': 'Anthrax Attacks',
    '2003-03-01': 'SARS Outbreak',
    '2006-06-01': 'HPV Vaccine Approval',
    '2009-04-01': 'H1N1 Pandemic',
    '2012-05-01': 'MERS Outbreak',
    '2014-08-01': 'Ebola Outbreak',
    '2015-02-01': 'Zika Virus Outbreak',
    '2017-08-01': 'CAR-T Cell Therapy Approval',
    '2020-03-01': 'COVID-19 Pandemic',
    '2021-12-01': 'Mass Vaccination Campaigns',
    '2022-12-01': 'COVID-19 Variants',
    '2023-03-01': 'Long COVID Research'
}

# Create a new column for event segments
data['Event'] = 'No Event'
for date, event in events.items():
    event_date = pd.to_datetime(date)
    data.loc[data.index >= event_date, 'Event'] = f"{event_date.year}"

# Exclude "No Event" from the data used for the plot
event_data = data[data['Event'] != 'No Event']

# Set the style of the visualization
sns.set(style='whitegrid')

# Create box plots for stock prices segmented by events with different colors
plt.figure(figsize=(10, 4))
ax = sns.boxplot(x='Event', y='ST-CM', data=event_data, palette='Set3')

# Ensure the x-axis labels are rotated for better readability
plt.xticks(rotation=90)

# Add legend manually
handles = [plt.Line2D([0], [0], color=color, marker='o', linestyle='', markersize=10) for color in sns.color_palette('Set3', len(events))]
labels = [f"{event} ({pd.to_datetime(date).year})" for date, event in events.items()]
plt.legend(handles, labels, title="Events", bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

# Set white background for plot and legend
ax.set_facecolor('white')
plt.gcf().set_facecolor('white')
plt.xlabel('Year')
plt.ylabel('Stock Price (ST-CM)')
plt.title('Stock Prices Segmented by Significant Events')

plt.tight_layout()

plt.savefig('Figures/boxplots.pdf', dpi = 300)

plt.show()



# =============================================================================
#  Event Windows 
# =============================================================================

# Load the data
data = aggregated_data.copy()
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Define the average closing stock price calculation
data['Average_Close'] = data[['ST-OM', 'ST-HM', 'ST-LM', 'ST-CM', 'ST-AM']].mean(axis=1)

# Define event dates with start, peak, and end periods
events = {
    'Anthrax Attacks': ('2001-10-01', '2001-10-15', '2001-10-30'),
    'SARS Outbreak': ('2003-03-01', '2003-03-15', '2003-03-30'),
    'HPV Vaccine Approval': ('2006-06-01', '2006-06-15', '2006-06-30'),
    'H1N1 Pandemic': ('2009-04-01', '2009-04-15', '2009-04-30'),
    'MERS Outbreak': ('2012-05-01', '2012-05-15', '2012-05-30'),
    'Ebola Outbreak': ('2014-08-01', '2014-08-15', '2014-08-30'),
    'Zika Virus Outbreak': ('2016-02-01', '2016-02-15', '2016-02-28'),
    'CAR-T Cell Therapy Approval': ('2017-08-01', '2017-08-15', '2017-08-30'),
    'COVID-19 Pandemic': ('2020-03-01', '2020-03-15', '2020-03-30'),
    'Mass Vaccination Campaigns': ('2020-12-01', '2020-12-15', '2020-12-30'),
    'COVID-19 Variants': ('2021-12-01', '2021-12-15', '2021-12-30'),
    'Long COVID Research': ('2023-03-01', '2023-03-15', '2023-03-30')
}

# Adjust the periods for the 30-day ranges
adjusted_events = {
    'Anthrax Attacks': ('2001-10-01', '2001-10-31', '2001-11-30'),
    'SARS Outbreak': ('2003-03-01', '2003-03-31', '2003-04-30'),
    'HPV Vaccine Approval': ('2006-06-01', '2006-06-30', '2006-07-31'),
    'H1N1 Pandemic': ('2009-04-01', '2009-04-30', '2009-05-31'),
    'MERS Outbreak': ('2012-05-01', '2012-05-31', '2012-06-30'),
    'Ebola Outbreak': ('2014-08-01', '2014-08-31', '2014-09-30'),
    'Zika Virus Outbreak': ('2016-02-01', '2016-02-29', '2016-03-31'), 
    'CAR-T Cell Therapy Approval': ('2017-08-01', '2017-08-31', '2017-09-30'),
    'COVID-19 Pandemic': ('2020-03-01', '2020-03-31', '2020-04-30'),
    'Mass Vaccination Campaigns': ('2020-12-01', '2020-12-31', '2021-01-31'),
    'COVID-19 Variants': ('2021-12-01', '2021-12-31', '2022-01-31'),
    'Long COVID Research': ('2023-03-01', '2023-03-31', '2023-04-30')
}

# Create subplots for each event window in a 3x4 grid
num_events = len(adjusted_events)
fig, axs = plt.subplots(4, 3, figsize=(18, 20), sharex=False)
axs = axs.flatten()

# Plot average closing stock price for each event window
colors = sns.color_palette("husl", num_events)
for i, (event, (start, peak, end)) in enumerate(adjusted_events.items()):
    start_date = pd.to_datetime(start) - pd.DateOffset(days=30)
    end_date = pd.to_datetime(end) + pd.DateOffset(days=30)
    
    window_data = data.loc[start_date:end_date]
    
    axs[i].plot(window_data.index, window_data['Average_Close'], label='Average Close Price', color='gray')
    axs[i].axvspan(pd.to_datetime(start), pd.to_datetime(peak), color=colors[i], alpha=0.3, label='Start to Peak')
    axs[i].axvspan(pd.to_datetime(peak), pd.to_datetime(end), color=colors[i], alpha=0.5, label='Peak to End')
    axs[i].set_title(f'{event}')
    axs[i].set_xlim([start_date, end_date])
    axs[i].legend(loc='upper left')

# Customizing the plot
for ax in axs:
    for label in ax.get_xticklabels():
        label.set_rotation(45)

plt.tight_layout()

plt.savefig('Figures/peak_figures_updated.pdf', dpi=300)

# Show the plot
plt.show()







