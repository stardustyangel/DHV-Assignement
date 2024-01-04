#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:17:13 2023

@author: tayssirboukrouba
"""

# importing the libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.gridspec import GridSpec


# setting the plot styles
sns.set(style="whitegrid")


def lineplot(df, x, y, countries, title, axis):
    '''
    Generates a line plot from a DataFrame with specified x and y columns, grouped by countries.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        countries (list): A list of country names to be included in the plot.
        title (str): The title of the line plot.

    Returns:
        None: Displays the line plot using the specified parameters.
    '''

    #fig, ax = plt.subplots(figsize=(10, 8))
    co_filter = df['Entity'].isin(countries)
    df_eu = df.loc[co_filter]
    sns.lineplot(data=df_eu, x=x, y=y, hue='Entity', errorbar=None, ax=axis)
    axis.set_xlim(1992, 2020)
    axis.axvline(2019, color='black', linestyle='--', label='Pendemic')
    axis.legend()
    axis.set_title(title, fontsize=16)


def hbarplot(df, x1, x2, y, title, xlabel, ylabel, axis):
    '''
    Generates a horizontal bar plot from a DataFrame with specified x1, x2, y columns.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        x1 (str): The column name for the first set of horizontal bar values.
        x2 (str): The column name for the second set of horizontal bar values.
        y (str): The column name for the y-axis values.
        title (str): The title of the horizontal bar plot.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.

    Returns:
        None: Displays the horizontal bar plot using the specified parameters.

    '''

    #plt.figure(figsize=(12, 8))
    data1 = df.groupby(y)[x1].mean()
    data2 = df.groupby(y)[x2].mean()

    x_axis = np.arange(len(data1.index))
    axis.barh(x_axis - 0.2, data1.values, 0.4, label='Consumption')
    axis.barh(x_axis + 0.2, data2.values, 0.4, label='Production')
    axis.set_yticks(x_axis, data1.index)
    axis.legend()
    axis.set_xlabel(xlabel)
    axis.set_ylabel(ylabel)
    axis.set_title(title, fontsize=16)


def pieplot(df, x, values1, values2, labels, title1, title2, title, axis):
    '''
    Generates a pie chart from a DataFrame with specified columns for labels, values1, and values2.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        x (str): The column name for the categorical variable used.
        values1 (str): The column name for the first set of values for the pie chart.
        values2 (str): The column name for the second set of values for the pie chart.
        labels (str): The labels associated with each pie slice.
        title1 (str): The title for the first set of values in the pie chart.
        title2 (str): The title for the second set of values in the pie chart.
        title (str): The overall title of the pie chart.

    Returns:
        None: Displays the pie chart using the specified parameters.

    '''

    mask = df[x].isin(labels)
    df_euru = df.loc[mask]
    df_euru1 = df_euru.groupby(x)[values1].sum()
    df_euru2 = df_euru.groupby(x)[values2].sum()

    autopct = '%.0f%%'
    explode = [0, 0, 0.2]

    axis[5].pie(df_euru1, labels=df_euru1.index,
                   autopct=autopct, explode=explode,radius=1.1)
    axis[5].set_title(title1,fontsize=16)
    axis[5].legend(loc='upper left')
    axis[6].pie(df_euru2, labels=df_euru2.index,
                   autopct=autopct, explode=explode,radius=1.1)
    axis[6].set_title(title2,fontsize=16)
    axis[6].legend(loc='upper left')

    


def barplot(df, x, y, labels, by, title, axis):
    '''
    Generates a bar plot from a DataFrame with specified x, y, labels, and grouping column.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        x (str): The column name for the x-axis values.
        y (str): The column name for the y-axis values.
        labels (str): The labels associated with each bar.
        by (str): The column name for grouping the data.
        title (str): The title of the bar plot.

    Returns:
        None: Displays the bar plot using the specified parameters.

    '''
    years = labels
    df = df.loc[df[by].isin(years)]
    sns.barplot(data=df, x=x, y=y, hue=by, errorbar=None, ax=axis)
    sns.despine(left=True)
    axis.set_title(title)


def radarplot(df, mask, categories, labels, color, title):
    '''
    Generates a radar plot from a DataFrame with specified categories, labels, and color.

    Parameters:
        df (DataFrame): The input DataFrame containing the data.
        mask (str): the mask filter to slice values to be used in the radar plot.
        categories (list): A list of column names for the radar plot axes.
        labels (list): A list of labels associated with each data point on the radar plot.
        color (str): Tthe color value associated with each data point.
        title (str): The title of the radar plot.

    Returns:
        None: Displays the radar plot using the specified parameters.

    '''
    euro_df = df.loc[mask]

    gas = np.log1p(euro_df[categories[0]].sum())
    oil = np.log1p(euro_df[categories[1]].sum())
    coal = np.log1p(euro_df[categories[2]].sum())

    values = [gas, oil, coal]
    plt.figure(figsize=(15, 8))

    num_types = len(labels)

    # Create a radar plot
    angles = np.linspace(0, 2 * np.pi, num_types, endpoint=False)
    values = np.concatenate((values, [values[0]]))  # Close the plot
    angles = np.concatenate((angles, [angles[0]]))  # Close the plot

    fig, axis = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    axis.fill(angles, values, color=color, alpha=0.5)

    axis.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    fig.suptitle(title)


# reading the csv file
df = pd.read_csv('fossil_use.csv')
print(df)

# EDA using decribe
print(df.describe())



# defining variables for radar plots (this is a bonus plot):
mask = (df['EURU'].isin(['EU']) & (df['Year'] > 2000))
categories = ['Gas consumption', 'Oil consumption', 'Coal consumption']
labels = ['Gas', 'Oil', 'Coal']
color = 'green'
title = 'Europe Total Consumption (log) Radar By Fuel Type (2000-2021)'

# calling the radarplot() function :
radarplot(df, mask, categories, labels, color, title)


fig = plt.figure(figsize=(30, 30))
fig.suptitle('Infographics Plots - 22084758', fontsize=70,fontfamily='sans-serif', fontname='DIN')

gs = GridSpec(4, 2, width_ratios=[1, 1], height_ratios=[
              1.5, 1.5, 1.5,2], wspace=0.3, hspace=0.3)
axs = [
    plt.subplot(gs[0, :]),
    plt.subplot(gs[1, 0]),
    plt.subplot(gs[1, 1]),
    plt.subplot(gs[2, 0]),
    plt.subplot(gs[2, 1]),
    plt.subplot(gs[3, 0]),
    plt.subplot(gs[3, 1])]

# defining columns for horizental bar plots :
df['Total Consumption'] = df['Coal consumption'] + \
    df['Oil consumption'] + df['Gas consumption']
df['Total Production'] = df['Coal production'] + \
    df['Oil production'] + df['Gas production']

# defining variables for horizental bar plots :
y = 'Region'
x1 = 'Total Consumption'
x2 = 'Total Production'
xlabel = 'Fuel Use'
ylabel = 'Regions'
title = 'Average Fossil Fuels Utilisation Across Regions'

# calling the hbarplot() function :
hbarplot(df, x1, x2, y, title, xlabel, ylabel,axs[0])


# defining variables for line plots :
x = 'Year'
y1 = 'Coal production'
y2 = 'Coal consumption'
countries = ['Germany', 'France',
             'United Kingdom', 'Italy', 'Russia', 'Ukraine']
title1 = 'Coal Production Across Europe'
title2 = 'Coal Consumption Across Europe'


# calling the lineplot() function :
lineplot(df, x, y1, countries, title1, axs[1])
lineplot(df, x, y2, countries, title2, axs[2])


# defining variables for pie plots :
x = 'EURU'
values1 = 'Gas production'
values2 = 'Gas consumption'
labels = ['EU', 'Russia', 'Ukraine']
title1 = 'Nautral Gas Production in Europe (1980-2021)'
title2 = 'Nautral Gas Consumption in Europe (1980-2021)'
title = 'Total Natural Gas Use in Europe '

# calling the pieplot() function :
pieplot(df, x, values1, values2, labels, title1, title2, title, axs)


# defining variables for bar plots :
labels = list(range(2010, 2020, 3))
by = 'Year'
x = 'Organizations'
y1 = 'Oil production'
y2 = 'Oil consumption'
title1 = 'Crude Oil Production By Organization'
title2 = 'Crude Oil Consumption By Organization'

# calling the barplot() function :
barplot(df, x, y1, labels, by, title1, axs[3])
barplot(df, x, y2, labels, by, title2, axs[4])



plt.savefig('22084758.png',dpi=300)