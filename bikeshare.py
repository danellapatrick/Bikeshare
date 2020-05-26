import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
    (str) city - name of the city to analyze
    (str) month - name of the month to filter by, or "all" to apply no month filter
    (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities_data = ('chicago', 'new york city', 'washington')
    while True:
        city = input(
            'Which of these cities do you want to explore : chicago , new york city  or washington? \n> ').lower()

        if city in cities_data:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input('Now you have to enter a month to get some months result \n> {} \n> '.format(months)).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    day = input('Now you have to enter a day to get some days result \n> {} \n> '.format(days)).lower()

    print('-' * 40)
    if month == '' and day == '':
        return city, months, days
    elif month == '' and day != '':
        return city, months, day
    elif month != '' and day == '':
        return city, month, days
    else:
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
    # this will read the data
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    month = df['Start Time'].dt.month.value_counts().idxmax()
    print('The most common month is {}'.format(month))

    # TO DO: display the most common day of week
    day = df['Start Time'].dt.weekday_name.value_counts().idxmax()
    print('The most common day of the week is {}'.format(day))
    # TO DO: display the most common start hour
    hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('The most common hour is {}'.format(hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].value_counts().reset_index()['index'][0]
    print('The most commonly used start station is: {}'.format(start_station))

    # TO DO: display most commonly used end station
    end_station = df['End Station'].value_counts().reset_index()['index'][0]
    print('The most commonly used end station is {}'.format(end_station))
    # TO DO: display most frequent combination of start station and end station trip

    frequent_stations = df.groupby(['Start Station'])['End Station'].value_counts().mode
    print('Most frequent start and end station: ', frequent_stations)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_sum = np.sum(df['Trip Duration'])
    total_travel_time = str(travel_sum).split()[0]
    print('The total travel time is {}'.format(total_travel_time))
    # TO DO: display mean travel time
    travel_avg = np.mean(df['Trip Duration'])
    avg_travel_time = str(travel_avg).split()[0]
    print('The total travel mean is {}'.format(avg_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('counts of user types \n{}'.format(user_type))
    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print('counts of gender \n{}'.format(gender))
    except:
        print('There is some error in data')

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        df['Birth Year'] = pd.to_datetime(df['Birth Year'])
        earliest = np.min(df['Birth Year'])
        most_recent = np.max(df['Birth Year'])
        birth = df['Birth Year'].dt.year.mode()
        print(
            ' Ther earliest {}, \n most recent{},\n most common year of birth {}'.format(earliest, most_recent, birth))
    except:
        print('There is some error in data')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-' * 40)


def display_raw_data(df):
    """
    Displays the data used to compute the stats
    Input:
        the dataframe with all the bikeshare data
    Returns:
       none
    """

    # omit auxiliary columns from visualization
    df = df.drop(['month', 'day_of_week'], axis=1)

    rowIndex = 0

    seeData = input(
        "\n Would you like to see rows of the data used to compute the stats? Please write 'yes' or 'no' \n").lower()

    while True:

        if seeData == 'no':
            return

        if seeData == 'yes':
            print(df[rowIndex: rowIndex + 5])
            rowIndex = rowIndex + 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()


