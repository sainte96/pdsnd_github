"""
Created on Sun Dec 12 00:33:30 2021
@author: omodara
"""

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the weekday to filter by, or "all" to apply no day filter
    """
    print('Hello!😊 Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Please enter the city you want to explore (chicago, new york city, washington): ")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print("opps! We are currently not in these cities, try chicago, new york city, washington.")
    # get user input for month (all, january, february, ... , june)
    while True:    
        month = input(city.capitalize() + "👍, nice! What month (January, February,...,June) do you want to explore in this location? Type 'all' if you would like to check for all months: ")
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Please select from first 6 months i.e January to June")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Do you want details specific to a particular day? If yes, type day name else type 'all': ")
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Please type in the weekday as in Monday, Tuesday etc.")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # use the index of the months list to get the corresponding int
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
        day = days.index(day)
        
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month= df['month'].mode()[0] - 1
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = months[month]
    
    day= df['day_of_week'].mode()[0]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday','sunday']
    day= days[day]
    
    print("The most common month is ", month.capitalize(), "\n")

    # display the most common day of week
    print("The most common day of week  is ", day.capitalize(), "\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['combination'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is", df['Trip Duration'].sum(), "\n")

    # display mean travel time
    print("The total mean time is", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['Gender'])['Gender'].count()
        print(gen)
        # Display earliest, most recent, and most common year of birth
        mryob = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        eyob = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        mcyob = df['Birth Year'].mode()[0]
        print("✅The Earliest year of birth is ", eyob, "\n")
        print("✅The most recent year of birth is ", mryob, "\n")
        print("✅The most common year of birth is ", mcyob, "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*30)
    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? type yes or no.\n')
        if raw.lower() == 'yes':
            print(df[x:x+5])
            x = x+5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? type yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()