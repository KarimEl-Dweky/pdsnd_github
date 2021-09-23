import time
import datetime
import pandas as pd
import random
import calendar 

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    
    month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    day_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    print("\nWelcome to BIKESHARE Data Analysis")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    check = 'y'
    while check == 'y':
        city = ""
        while city not in CITY_DATA.keys():
            print("\nKindly enter the required City: ")
            
            city = input().lower()
        
            if city not in CITY_DATA.keys():
                print("\nPlease enter only one of the following cities:\
                        \n1. Chicago 2. New York City 3. Washington")
        

    # TO DO: get user input for month (all, january, february, ... , june)
    
        month = ""
        while month not in month_dict.keys():
            print("\nFor Filtering : Kindly enter the required Month between (January to June)\
                    \nYou may also enter (All) to view data for all months:")
            
            month = input().lower()
        
            if month not in month_dict.keys():
                print("\nNot a month or all")
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
        day = ""
        while day not in day_list:
            print("\nFor Filtering: Kindly enter the required Day Of the Week\
                    \nYou may also enter (All) to view data for all days of the week:")
            
            day = input().lower()
        
            if day not in day_list:
                print("\nNot a day or all")
        
        print("\nYou have entered {} as your City choice".format(city.title()))
        print("You have entered {} as your Month filter choice".format(month.title()))
        print("You have entered {} as your day filter choice".format(day.title()))
        
        check = input("\nWould you like to change your entry? (y or n) ") 

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
    # loading data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'], infer_datetime_format=True)
    
    # extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filtering by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filtering by month to create the new dataframe
        df = df[df['month'] == month]
    
    # filtering by day of week if applicable
    if day != 'all':
        # filtering by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculating the most common month
    most_common_month = calendar.month_name[df['month'].value_counts().idxmax()]
    print('The Most Common Month: ', most_common_month)

    # Calculating the most common day of week
    most_common_day = df['day_of_week'].value_counts().idxmax()
    print('The Most Common Day: ', most_common_day)

    # Calculating the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].value_counts().idxmax()
    print('The Most Frequent Start Hour: {} ({})'.format(most_common_start_hour, datetime.time(most_common_start_hour).strftime("%I:00 %p")))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Calculating most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print("The Most Commonly Used Start Station: ", common_start_station)

    # Calculating most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print("The Most Commonly Used End Station: ", common_end_station)

    # Calculating most frequent combination of start station and end station trip
    df['Start-End'] = df[['Start Station', 'End Station']].agg(' -- '.join, axis=1)
    common_start_to_end = df['Start-End'].value_counts().idxmax()
    print("The Most frequent Used TRIP from Start to End Stations : ", common_start_to_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculating total travel time
    total_travel_time = df['Trip Duration'].sum()
    m, s = divmod(total_travel_time, 60)
    h, m = divmod(m, 60)
    print("Total Travel Time in Seconds: {} Seconds".format(total_travel_time))
    print("The Total Travel Time is {} Hours, {} Minutes and {} Seconds.".format(h, m, s))

    # Calculating mean travel time
    mean_travel_time = df['Trip Duration'].mean().round()
    m, s = divmod(mean_travel_time, 60)
    h, m = divmod(m, 60)
    print("The Average Travel Time in Seconds: {} seconds".format(mean_travel_time))
    print("The Average Travel Time is {} hours, {} minutes and {} seconds.".format(h, m, s))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Calculating counts of user types
    user_types_counts = df['User Type'].value_counts()
    print("The Counts of User Types as follow:\n{}".format(user_types_counts))

    # Calculating counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("\nThe counts of Genders as follow:\n{}".format(gender_counts))
    except:
        print("\nThere is no 'Gender' column in this city file.")
        
    # Calculating earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].value_counts().idxmax())
        print("\nThe Earliest Year Of Birth: {}".format(earliest))
        print("The Most Recent Year of Birth: {}".format(most_recent))
        print("The Most Common Year of Birth: {}".format(most_common))
    except:
        print("There are no 'Birth Year' column in this city file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    '''Displays 5 rows of data from the csv file for the selected city.'''
    print('\nDisplaying Some Raw Data...\n')

    check = 'y'
    while check == 'y':
        print("\nWould you like to view the raw data? (y or n)")
        
        raw_data = input().lower()
        
        if raw_data == 'y':
            print(df.head())
            sample_data = 'y'
            while sample_data == 'y':
                print("\nWould you like to view more raw data? (y or n)")
                sample_data = input().lower()
                if sample_data == "y":
                    print(df.sample(5))
                elif sample_data != "y":
                    check = 'n'
                    break
        elif raw_data == 'n':
            break
        elif raw_data != ('y' or 'n'):
            print("\nInput does not seem to match any of the accepted responses.")
        
            
    print('-'*80)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else:
            print('-'*80)


if __name__ == "__main__":
	main()
