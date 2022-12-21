"""
This python script implements the solution for the Explore US Bikeshare Data problem in
Udacity course programming for data science with Python.
It uses pandas an the underlying numpy for data processing.
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Ductionaries for data input and mappings
CITY_INPUT = { '0': 'chicago',
               '1': 'new york city',
               '2': 'washington'}

MONTH_INPUT = { '0': 'all',
                '1': 'january',
                '2': 'february',
                '3': 'march',
                '4': 'april', 
                '5': 'may',
                '6': 'june'}

WEEKDAY_INPUT = {'0': 'all',
                 '1': 'monday',
                 '2': 'tuesday',
                 '3': 'wednesday',
                 '4': 'thursday',
                 '5': 'friday',
                 '6': 'saturday',
                 '7': 'sunday'}

    
def generate_input_message(type, dict):
    """
    Prepares a string to be used as input to the end user.
    The string is based on a configuration dictionary and provides a
    simple menu.

    Parameters:
        (str) type : menu tpye under processing;
        (dic) dict : key mappings.

    Returns
        (str) message: Input message formatted.

    """

    message = ', '.join(key + ' -> ' + value for key, value in dict.items())
    message = f'SELECT a {type} ID from ({message}): '
    return message


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) weekday - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city, rules in CITY_INPUT dict
    city = ''
    while city not in CITY_INPUT.keys():
        city = input(generate_input_message('CITY', CITY_INPUT))

    # get user input for month, rules in MONTH_INPUT dict
    month = ''
    while month not in MONTH_INPUT.keys():
        month = input(generate_input_message('MONTH', MONTH_INPUT))
        
    # get user input for weekday, rules in WEEKDAY_INPUT dict
    weekday = ''
    while weekday not in WEEKDAY_INPUT.keys():
        weekday = input(generate_input_message('WEEKDAY', WEEKDAY_INPUT))
        
    print(f'Selected city [{CITY_INPUT[city]}], month [{MONTH_INPUT[month]}] and weekday [{WEEKDAY_INPUT[weekday]}]!')

    print('-'*40)
    return CITY_INPUT[city], MONTH_INPUT[month], WEEKDAY_INPUT[weekday]


def load_data(city, month, weekday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) weekday - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    
    # convert Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # create month and weekday columns from Start Time
    # January is 1, ... December 12 as in MONTH_INPUT
    df['Month'] = df['Start Time'].dt.month
    # Monday is 0, ... Sunday is 6, adding 1 to coupe with WEEKDAY_INPUT
    df['Weekday'] = df['Start Time'].dt.weekday + 1
    # Hour start event
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':       
        # filter by month to create the new dataframe, using MONTH_INPUT dict
        month_id = int([k for k, v in MONTH_INPUT.items() if v == month][0])
        df = df[df['Month'] == month_id]

    # filter by weekday if applicable
    if weekday != 'all':
        # filter by weekday to create the new dataframe, using WEEKDAY_INPUT dict
        weekday_id = int([k for k, v in WEEKDAY_INPUT.items() if v == weekday][0])
        df = df[df['Weekday'] == weekday_id]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_com_month = str(df['Month'].mode()[0])
    print(f'Most common month: {MONTH_INPUT[most_com_month]}')

    # display the most common weekday
    most_com_weekday = str(df['Weekday'].mode()[0])
    print(f'Most common weekday: {WEEKDAY_INPUT[most_com_weekday]}')

    # display the most common start hour
    most_com_hour = df['Hour'].mode()[0]
    print(f'Most common hour: {most_com_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_com_start_station = str(df['Start Station'].mode()[0])
    print(f'Most common Start Station: {most_com_start_station}')

    # display most commonly used end station
    most_com_end_station = str(df['End Station'].mode()[0])
    print(f'Most common End Station: {most_com_end_station}')

    # display most frequent combination of start station and end station trip
    most_com_comb = df.groupby(['Start Station', 'End Station']).size().nlargest(1).index[0]
    print(f'Most common combination Start -> End Station: {most_com_comb[0]} -> {most_com_comb[1]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f'Total travel time: {total_travel_time} s')

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f'Mean travel time: {mean_travel_time } s')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f'User type counts:\n {user_types}')

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'Gender counts:\n {gender_counts}')
    else:
        print('Gender is not available for the city data!')
        

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_yob = int(df['Birth Year'].min())
        max_yob = int(df['Birth Year'].max())
        most_com_yob = int(df['Birth Year'].mode())
        print(f'Earliest year of birth: {min_yob}')
        print(f'Most recent year of birth: {max_yob}')
        print(f'Most common year of birth: {most_com_yob}')
    else:
        print('Birth Year is not available for the city data!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Manages the display of the filtered dataset available after dumping the statistics.
    The user is able to dump 5 rows of data at each time.

    Parameters:
        (dataframe) df : The filtered dataframe after applying the required initial conditions.
    """    

    view_data = 'n'
    position = 0
    add_message = "the first"
    first_message = True
    
    while True:
        view_data = input(f'\nDisplay {add_message} 5 rows of data (y -> yes, n -> no)? ').lower()
        if view_data == 'y':
            print(df.iloc[position:position + 5])
            position += 5       
            if first_message:
                first_message = False
                add_message = "the next"

        if view_data == 'n':
            break
    

def main():
    while True:
        city, month, weekday = get_filters()
        df = load_data(city, month, weekday)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = ' '
        while restart not in ['y', 'n']:
            restart = input('\nWould you like to restart (y -> yes, n -> no)? ').lower()
        if restart.lower() == 'n':
            break

if __name__ == "__main__":
	main()
