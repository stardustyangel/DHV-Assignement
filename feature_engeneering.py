#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 09:50:07 2023

@author: tayssirboukrouba
"""
# importing the libraries 
import pandas as pd

#reading the dataframe
df = pd.read_csv('Fuel production vs consumption.csv')

#cleaning the dataframe 
df.fillna(0, inplace=True)
myfilter = df['Year'].isin(list(range(1980, 2022)))
df = df.loc[myfilter]
values_to_drop = ['Antarctica', 'Cook Islands', 'Czechoslovakia', 'Faeroe Islands',
                  'Former Serbia and Montenegro', 'Former U.S.S.R.', 'Former Yugoslavia',
                  'French Polynesia', 'Hawaiian Trade Zone', 'Macao', 'Montserrat',
                  'Northern Mariana Islands', 'Reunion', 'Saint Helena', 'U.S. Territories', 'West Germany', 'World']
df = df[~df['Entity'].isin(values_to_drop)]


# Defining a function to classify countries into organisations
def classify_organization(country):
    if country in ['Saudi Arabia', 'Iran', 'Iraq', 'Venezuela', 'Nigeria', 'Algeria', 'Kuwait', 'UAE', 'Libya', 'Gabon', 'Congo']:
        return 'OPEC'
    elif country in ['Brazil', 'Russia', 'India', 'China', 'South Africa']:
        return 'BRICS'
    elif country in ['USA', 'Canada', 'Japan', 'Germany', 'UK', 'France', 'Italy']:
        return 'G7'
    else:
        return 'Other'

# Defining a function to classify countries into regions
def classify_regions(country):
    if country in ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi',
                   'Cameroon', 'Cape Verde', 'Central African Republic', 'Chad', 'Comoros',
                   'Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Eswatini',
                   'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Tanzania',
                   'Cote d\'Ivoire', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Tunisia', 'Western Sahara',
                   'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Togo',
                   'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Rwanda', 'Sao Tome and Principe',
                   'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'Uganda',
                   'Zambia', 'Zimbabwe', 'Democratic Republic of Congo', 'South Sudan', 'Sudan']:
        return 'Africa'
    
    elif country in ['Afghanistan', 'Armenia', 'Azerbaijan', 'Bahrain', 'Iran', 'Iraq', 'Israel', 'Jordan',
                         'Kuwait', 'Lebanon', 'Oman', 'Palestine', 'Qatar', 'Saudi Arabia', 'Syria',
                         'United Arab Emirates', 'Yemen'] : 
        return 'Middle East'

    elif country in ['Bangladesh', 'Bhutan', 'Brunei', 'Cambodia', 'China', 'Georgia', 'Hong Kong', 'India',
                   'Indonesia', 'Japan', 'Kazakhstan', 'Kyrgyzstan', 'Laos', 'Macau', 'Malaysia', 'Maldives',
                   'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 'Pakistan', 'Philippines', 'Singapore',
                   'South Korea', 'Sri Lanka', 'Taiwan', 'Tajikistan', 'Thailand', 'Timor', 'Turkmenistan',
                   'Uzbekistan', 'Vietnam']:
        return 'East Asia'
    elif country in ['Albania', 'Andorra', 'Austria', 'Belarus', 'Belgium',
                     'Bosnia and Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
                     'Denmark', 'Estonia', 'Faroe Islands', 'Finland', 'France', 'Georgia',
                     'Germany', 'Gibraltar', 'Greece', 'Greenland', 'Hungary', 'Iceland', 'Ireland',
                     'Italy', 'Kosovo', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                     'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino', 'Serbia',
                     'Slovakia', 'Slovenia', 'Spain', 'Svalbard and Jan Mayen', 'Sweden',
                     'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City', 'Turkey']:
        return 'Europe'
    elif country in ['American Samoa', 'Antigua and Barbuda', 'Aruba', 'Bahamas', 'Barbados', 'Belize', 'Bermuda',
                            'Canada', 'Cayman Islands', 'Cuba', 'Dominica', 'Dominican Republic', 'East Germany',
                            'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Haiti', 'Honduras',
                            'Jamaica', 'Martinique', 'Mexico', 'Netherlands Antilles', 'Nicaragua', 'Panama',
                            'Puerto Rico', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Pierre and Miquelon',
                            'Saint Vincent and the Grenadines', 'Turks and Caicos Islands', 'United States',
                            'United States Virgin Islands']:
        return 'North America'
    
    elif country in ['Argentina', 'Bolivia', 'Brazil', 'British Virgin Islands', 'Chile', 'Colombia',
                            'Costa Rica', 'Ecuador', 'El Salvador', 'Falkland Islands', 'French Guiana', 'Guyana',
                            'Honduras', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Suriname',
                            'Trinidad and Tobago', 'Uruguay', 'Venezuela'] : 
        return 'South America'
    elif country in [
        'Australia', 'Fiji', 'Kiribati', 'Micronesia (country)', 'Nauru',
        'New Caledonia', 'New Zealand', 'Niue', 'Palau', 'Papua New Guinea', 'Samoa',
        'Solomon Islands', 'Tokelau', 'Tonga', 'Tuvalu', 'U.S. Pacific Islands',
            'Vanuatu', 'Wake Island']:
        return 'Oceania'
    else:
        return 'Other'

# Defining a function to classify countries into EU countries
def classify_eu(country):
    eu_countries = [
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy',
        'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal',
        'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']

    if country in eu_countries:
        return 'EU'
    if country in 'Russia':
        return 'Russia'
    if country in 'Ukraine':
        return 'Ukraine'
    else:
        return 'Other'


df['Organizations'] = df['Entity'].apply(classify_organization)
df['Region'] = df['Entity'].apply(classify_regions)
df['EURU'] = df['Entity'].apply(classify_eu)

df.to_csv('fossil_use.csv', index=False)
