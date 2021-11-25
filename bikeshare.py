
import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, week and/or weekday to analyze.

    Args:
        n/a

    Returns:
        (str) city - name of the city to analyze, or None for all cities
        (str) month - name of the month to filter by, or None for all month
        (int) week - number if the calendar week to filter by, or None for all calendar weeks
        (str) day - name of the weekday to filter by, or None for all weekdays

    """

    print("\nHello! Let's explore some US bikeshare data!\n")

    # Create default filter selection
    city = None
    month = None
    week = None
    day = None

    # Create error message
    sorry = "Sorry, your selection could not be processed. Please give it another try!\n\n"

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    list_of_valid_answers = ["chicago", "newyork", "new york", "newyorkcity", "new york city", "washington", "all", ""]
    while True:
        city = input("\nWhich city do you want to see data for?\n | Divvy is located in Chicago, New York City and Washington. You can also type in 'all' to see data for all cities.\n\n Please enter your selection: ")
        city = city.lower()
        if city in list_of_valid_answers:
            break
        print(sorry)

    if city != "": print(" Thank you!")

    if (city == "all") or (city == ""):
        city = None
        city_statement =  "you'll get to see the data from all our cities"
    else:
        if (city == "newyork") or (city == "new york") or (city == "newyorkcity"): city = "new york city"
        city_statement = "you'll get to see the {} data".format(city.title())

    # TO DO: get user input for month (all, january, february, ... , june)
    list_of_valid_answers = ["january", "february", "march", "april", "may", "june", "all", ""]
    while True:
        month = input("\nWhich month do you want to see data for?\n | Data is available for the months January through June. You can also type in 'all' to see data for the enitre timespan.\n | If you rather want to select a specific calendar week in the next step you can just hit Enter wihtout any input.\n\n Please enter your selection: ")
        month = month.lower()
        if month in list_of_valid_answers:
            break
        print(sorry)

    if month != "": print(" Thank you!")

    if (month == "all") or (month == ""):
        month = None
        month_statement = ",\n over the entire timespan, from January through June"
    else: month_statement = ",\n over the month of {}".format(month.title())

    # TO DO: get user input for week (1, 2, ... , 26)
    max_cw_available = 26
    while True:
        week = input("\nWhich week do you want to see data for?\n | Data is available trough calendar week 26. Just type in the number of the calendar week.\n | If you select a calendar week, this will overwrite a selected month. Both will not work.\n | If you want to keep the selected month, you can just hit Enter without any input.\n\n Please enter your selection: ")
        if week == "":
            week = None
            break
        else:
            try:
                week = int(week)
                if week <= max_cw_available:
                    break
            except: print(sorry)
            print(sorry)

    week_statement = ""
    if week != None:
        print(" Thank you!")
        month_statement = ""
        week_statement = "\n over calendar week {}".format(week)

    # TO DO: get user input for day of week (all, monday, tuesday, ... , sunday)
    list_of_valid_answers = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" , "all", ""]
    while True:
        day = input("\nWhich weekday do you want to see data for?\n | Data is available for all weekdays from Monday through Sunday. You can also type in 'all' to see data for the all weekdays.\n\n Please enter your selection: ")
        day = day.lower()
        if day in list_of_valid_answers:
            break
        print(sorry)

    if day != "": print(" Thank you!")

    if (day == "all") or (day == ""):
        day = None
        #day_statement = ",\n including all weekdays."
        day_statement = "."
    else: day_statement = ", for the weekday {}.".format(day.title())

    # Create some fix filter selections for testing
    #city = "chicago"; month = "february"; day = "friday"
    #city = "chicago"; month = "february"; week = 8
    #city = "chicago"; week = 7; day = "saturday"
    #city = "chicago"; week = 52
    #week = 26
    #day = monday
    #city = None; month = None; week = None; day = None
    #city = "washington"

    # Print the filter selection
    # print("\nfilter selection = \n city = {}\n month = {}\n week = {}\n day = {}\n".format(city, month, week, day))

    # Print the filter selection statement
    print("\n\nOkay, " + city_statement + month_statement + week_statement + day_statement)
    input("\n Let's go? ... Hit Enter!")
    print('-'*40)
    print('\nLoading Divvy source data...\n')

    print('-'*40)
    return city, month, week, day



def load_data(city, month, week, day):
    """
    Loads data for the specified city or cities and filters by month, week and/or weekday.
    If no specific city is requested, data for all cities is provided.
    Filtering is allowed for month or weeks, not both.

    Args:
        (str) city - name of the city to analyze, or None for all cities
        (str) month - name of the month to filter by, or None for all month
        (int) week - number if the calendar week to filter by, or None for all calendar weeks
        (str) day - name of the weekday to filter by, or None for all weekdays

    Returns:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Comment:
        The load_data function works exactly like in the practice #3 section!
        With a little extra spice.

    """

    # Load data for requested city in dataframe and add 'City' column
    if city != None:
        df = pd.read_csv(CITY_DATA[city])
        df['City'] = city.title()

    # Load data for all cities in dataframe and add 'City' column
    else:
        # print("number of CITY_DATA files =", len(CITY_DATA))
        city_data_keys = CITY_DATA.keys()
        # print("city_data_keys =", city_data_keys)
        union_list = []

        for key in city_data_keys:
            df = pd.read_csv(CITY_DATA[key])
            df['City'] = key.title()
            union_list.append(df)

        df = pd.concat(union_list, ignore_index=True, sort=False, copy=False)#; print("df = \n", df)

    # Convert the start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])#; print("\nmax df['Start Time'] = {}\nmin df['Start Time'] = {}".format(max(df['Start Time']), min(df['Start Time'])))
    df['End Time'] = pd.to_datetime(df['End Time'])#; print("\nmax df['End Time'] = {}\nmin df['End Time'] = {}".format(max(df['End Time']), min(df['End Time'])))

    # Create columns for month, week, day, hour based on Start Time and trip from to destinations
    df['Month'] = df['Start Time'].dt.month#; print("\nmax df['Month'] = {}\nmin df['Month'] = {}".format(max(df['Start Time']).month, min(df['Start Time']).month))#; print("\ndf['Month'] = \n", df['Month'])
    df['Week'] = df['Start Time'].dt.week#; print("\nmax df['Week'] = {}\nmin df['Week'] = {}".format(max(df['Start Time']).week, min(df['Start Time']).week))#; print("\ndf['Week'] = \n", df['Week'])
    df['Day of Week'] = df['Start Time'].dt.dayofweek#; print("\ndf['Day of Week'] = \n", df['Day of Week'])
    df['Hour'] = df['Start Time'].dt.hour#; print("\nmax df['Hour'] = {}\nmin df['Hour'] = {}".format(max(df['Start Time']).hour, min(df['Start Time']).hour))#; print("\ndf['Hour'] = \n", df['Hour'])
    df['Trip From To'] = df['Start Station']+" to "+df['End Station']#; print("\ndf['Trip From To'] = \n", df['Trip From To'])

    # Filter dataframe to requested month or week - requesting all or nothing results in getting all the data, i.e. no filtering
    # Use if conditions to choose weeks over month and respect a week that lives in two different months
    if week != None:
        # Filter by calendar week number and create new dataframe
        df = df.loc[df['Week'] == week]#; print("\ndf filtered by week {} = \n".format(week), df)
    else:
        if month != None:
            # Filter by list index of months and create new dataframe
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month_index = months.index(month)+1#; print("month_index = ", month_index)
            df = df.loc[df['Month'] == month_index]#; print("\ndf filtered by month {} = \n".format(month_index), df)

    # Filter dataframe to requested day - requesting all or nothing results in getting all the data, i.e. no filtering
    if day != None:
        # Filter by list index of days and create new dataframe
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day_index = days.index(day)#; print("day_index = ", day_index)
        df = df.loc[df['Day of Week'] == day_index]#; print("\ndf filtered by Day of Week {} = \n".format(day_index), df)

    # Check timespan - does it match the selected month or week or day?
    if df.empty: print("\nThere is no data available for your selection.")
    # else: print("\ntimespan to check return df =\n filtered max(df['Start Time']) = {}\n filtered min(df['Start Time']) = {}".format(max(df['Start Time']), min(df['Start Time'])))

    return df



def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Returns:
        n/a

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # print("\ndf['Month'].value_counts() = \n", df['Month'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Month'].nunique()
    top = df['Month'].mode()[0]
    name = calendar.month_name[top]
    travels = df['Month'].value_counts()[top]
    # Print result statement
    print(" | Out of {} months in total, {} was the most common month, with {} travels.".format(total, name, travels))

    # Display the most commen week
    # print("\ndf['Week'].value_counts() = \n", df['Week'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Week'].nunique()
    top = df['Week'].mode()[0]
    name = "CW " +str(top)
    travels = df['Week'].value_counts()[top]
    # Print result statement
    print(" | Out of {} weeks in total, {} was the most common week, with {} travels.".format(total, name, travels))

    # TO DO: display the most common day of week
    # print("\ndf['Day of Week'].value_counts() = \n", df['Day of Week'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Day of Week'].nunique()
    top = df['Day of Week'].mode()[0]
    name = calendar.day_name[top]
    travels = df['Day of Week'].value_counts()[top]
    # Print result statement
    print(" | Out of {} weekdays in total, {} was the most common day, with {} travels.".format(total, name, travels))

    # TO DO: display the most common start hour
    # print("\ndf['Hour'].value_counts() = \n", df['Hour'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Hour'].nunique()
    top = df['Hour'].mode()[0]
    name = str(top)+"-"+str(top+1)
    travels = df['Hour'].value_counts()[top]
    # Print result statement
    print(" | Out of {} start hours in total, {} o'clock was the most common start hour, with {} travels.".format(total, name, travels))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input("\n Are you ready for The Most Popular Stations and Trip? ... Hit Enter!")



def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

    Args:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Returns:
        n/a

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    # print("\ndf['Start Station'].value_counts() = \n", df['Start Station'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Start Station'].nunique()
    top = df['Start Station'].mode()[0]
    name = top
    travels = df['Start Station'].value_counts()[top]
    # Print result statement
    print(" | Out of {} start stations in total, {} was the most common start station, with {} travels.".format(total, name, travels))

    # TO DO: display most commonly used end station
    # print("\ndf['End Station'].value_counts() = \n", df['End Station'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['End Station'].nunique()
    top = df['End Station'].mode()[0]
    name = top
    travels = df['End Station'].value_counts()[top]
    # Print result statement
    print(" | Out of {} end stations in total, {} was the most common end station, with {} travels.".format(total, name, travels))

    # TO DO: display most frequent combination of start station and end station trip
    # print("\ndf['Trip From To'].value_counts() = \n", df['Trip From To'].value_counts())
    # Get number of unique values, get the most frequent, get it's name, get it's number of travels
    total = df['Trip From To'].nunique()
    top = df['Trip From To'].mode()[0]
    name = top
    travels = df['Trip From To'].value_counts()[top]
    # Print result statement
    print(" | Out of {} trip combinations in total, {} was the most common combination, with {} travels.".format(total, name, travels))

    # Emphasize if it is the same start and end station
    if df['Start Station'].mode()[0] == df['End Station'].mode()[0]:
        print(" |\n | Note that for this selection, {} is both the most common start and end station!".format(df['End Station'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input("\n Are you ready for Trip Duration? ... Hit Enter!")



def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

    Args:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Returns:
        n/a

    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    result = df['Trip Duration'].sum()#; print("\ndf['Trip Duration'].dtypes = {}\ndf['Trip Duration'].sum() = {} seconds".format(df['Trip Duration'].dtypes, result))
    # Create some small local functions for calculating floats, floors and decimals out of result and divider
    def get_float(result, divider): return result/divider
    def get_floor(result,divider): return result//divider
    def get_decimal(result, divider): return result%divider/divider
    def get_int(result, divider): return int(result//divider)
    def get_travel_time(result, divider, name):
        this_float = get_float(result, divider)
        this_floor = get_floor(result, divider)
        this_decimal = get_decimal(result, divider)
        this_int = get_int(result, divider)
        # print("\nWith {}_divider = {} get_travel_time() returns\n {}_float = {}\n {}_floor ={}\n {}_decimal = {}\n {}_int = {}".format(name, divider, name, this_float, name, this_floor, name, this_decimal, name, this_int))
        return this_float, this_floor, this_decimal, this_int
    # Create another small local function for the result statement
    def add_to_statement(input_value, name):
        addition = ""
        if input_value >0:
            addition = " {} {}".format(input_value, name)
            if input_value >1: addition += "s"
        return addition
    """
    Is the small local functions section a good approach? I wanted to keep things in 1 line that fit in 1 line. My thought was visual clarity > documentation of a one-liner. Let me know!

    """
    # Create result statement
    result_statement = " | The total travel time is"
    # Calculate years values and add result statement
    years_float, years_floor, years_decimal, years_int = get_travel_time(result, 60*60*24*365, "years")
    result_statement += add_to_statement(years_int, "year")
    # Calculate months values and add result statement
    months_float, months_floor, months_decimal, months_int = get_travel_time(years_decimal, 1/12, "months")
    result_statement += add_to_statement(months_int, "month")
    # Calculate days values and add result statement
    days_float, days_floor, days_decimal, days_int = get_travel_time(months_decimal, 1/30, "days")
    result_statement += add_to_statement(days_int, "day")
    # Calculate hours values and add result statement
    hours_float, hours_floor, hours_decimal, hours_int = get_travel_time(days_decimal, 1/24, "hours")
    result_statement += add_to_statement(hours_int, "hour")
    # Calculate minutes values and add result statement
    minutes_float, minutes_floor, minutes_decimal, minutes_int = get_travel_time(hours_decimal, 1/60, "minutes")
    result_statement += add_to_statement(minutes_int, "minute")
    # Calculate seconds values and add result statement
    seconds_float, seconds_floor, seconds_decimal, seconds_int = get_travel_time(minutes_decimal, 1/60, "seconds")
    result_statement += add_to_statement(seconds_int, "second")
    result_statement += "."
    # Print result statement
    print(result_statement)

    """
    >>> DEPRECATED IN FAVOR OF THE SOME SMALL FUNCTIONS APPROACH ABOVE <<<

    # Calculate year values
    divider = 60*60*24*365; print("\ndivider = ", divider)
    years_float = result/divider; print("years_float = ", years_float)
    years_floor = result//divider; print("years_floor = ", years_floor)
    years_decimal = result%divider/divider; print("years_decimal = ", years_decimal)
    years_int = int(years_floor); print("years_int = ", years_int)
    # Calculate month values
    result = years_decimal
    divider = 1/12; print("\ndivider = ", divider)
    months_float = result/divider; print("months_float = ", months_float)
    months_floor = result//divider; print("months_floor = ", months_floor)
    months_decimal = result%divider/divider; print("months_decimal = ", months_decimal)
    months_int = int(months_floor); print("months_int = ", months_int)
    # Calculate day values
    result = months_decimal
    divider = 1/30; print("\ndivider = ", divider)
    days_float = result/divider; print("days_float = ", days_float)
    days_floor = result//divider; print("days_floor = ", days_floor)
    days_decimal = result%divider/divider; print("days_decimal = ", days_decimal)
    days_int = int(days_floor); print("days_int = ", days_int)
    # Calculate hour values
    result = days_decimal
    divider = 1/24; print("\ndivider = ", divider)
    hours_float = result/divider; print("hours_float = ", hours_float)
    hours_floor = result//divider; print("hours_floor = ", hours_floor)
    hours_decimal = result%divider/divider; print("hours_decimal = ", hours_decimal)
    hours_int = int(hours_floor); print("hours_int = ", hours_int)
    # Calculate minute values
    result = hours_decimal
    divider = 1/60; print("\ndivider = ", divider)
    minutes_float = result/divider; print("minutes_float = ", minutes_float)
    minutes_floor = result//divider; print("minutes_floor = ", minutes_floor)
    minutes_decimal = result%divider/divider; print("minutes_decimal = ", minutes_decimal)
    minutes_int = int(minutes_floor); print("minutes_int = ", minutes_int)
    # Calculate second values
    result = minutes_decimal
    divider = 1/60; print("\ndivider = ", divider)
    seconds_float = result/divider; print("seconds_float = ", seconds_float)
    seconds_floor = result//divider; print("seconds_floor = ", seconds_floor)
    seconds_decimal = result%divider/divider; print("seconds_decimal = ", seconds_decimal)
    seconds_int = int(seconds_floor); print("seconds_int = ", seconds_int)
    """

    """
    >>> DEPRECATED IN FAVOR OF THE OTHER SMALL FUNCTION ABOVE <<<

    result_statement = " | The total travel time was "
    if years_int >0:
        result_statement += "{} years".format(years_int)
        if years_int >1: result_statement += "s"
        result_statement += ", "
    if months_int >0:
        result_statement += "{} month".format(months_int)
        if months_int >1: result_statement += "s"
        result_statement += ", "
    if days_int >0:
        result_statement += "{} day".format(days_int)
        if days_int >1: result_statement += "s"
        result_statement += ", "
    if hours_int >0:
        result_statement += "{} hour".format(hours_int)
        if hours_int >1: result_statement += "s"
        result_statement += ", "
    if minutes_int >0:
        result_statement += "{} minute".format(minutes_int)
        if minutes_int >1: result_statement += "s"
        result_statement += " and "
    if seconds_int >0:
        result_statement += "{} second".format(seconds_int)
        if seconds_int >1: result_statement += "s"
        result_statement += "."
    """

    # TO DO: display mean travel time
    result = df['Trip Duration'].mean()    #; print("\ndf['Trip Duration'].dtypes = {}\ndf['Trip Duration'].mean() = {} seconds".format(df['Trip Duration'].dtypes, result))
    # Create result statement
    result_statement = " | The mean travel time is"
    # Calculate years values and add result statement
    years_float, years_floor, years_decimal, years_int = get_travel_time(result, 60*60*24*365, "years")
    result_statement += add_to_statement(years_int, "year")
    # Calculate months values and add result statement
    months_float, months_floor, months_decimal, months_int = get_travel_time(years_decimal, 1/12, "months")
    result_statement += add_to_statement(months_int, "month")
    # Calculate days values and add result statement
    days_float, days_floor, days_decimal, days_int = get_travel_time(months_decimal, 1/30, "days")
    result_statement += add_to_statement(days_int, "day")
    # Calculate hours values and add result statement
    hours_float, hours_floor, hours_decimal, hours_int = get_travel_time(days_decimal, 1/24, "hours")
    result_statement += add_to_statement(hours_int, "hour")
    # Calculate minutes values and add result statement
    minutes_float, minutes_floor, minutes_decimal, minutes_int = get_travel_time(hours_decimal, 1/60, "minutes")
    result_statement += add_to_statement(minutes_int, "minute")
    # Calculate seconds values and add result statement
    seconds_float, seconds_floor, seconds_decimal, seconds_int = get_travel_time(minutes_decimal, 1/60, "seconds")
    result_statement += add_to_statement(seconds_int, "second")
    result_statement += "."
    # Print result statement
    print(result_statement)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    input("\n Are you ready for User Stats? ... Hit Enter!")



def user_stats(df):
    """
    Displays statistics on bikeshare users.

    Args:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Returns:
        n/a

    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Check df for existing values in specific columns
    # print("\ndf = \n", df.count())
    total_count = df.shape[0]#; print("df.shape[0] = ", total_count)

    # TO DO: Display counts of user types
    # print("\ndf['User Type'].value_counts() = \n", df['User Type'].value_counts())
    # Check column for existing values
    value_count = df['User Type'].count()#; print("df['User Type'].count() = ", value_count)
    nan_count = df['User Type'].isna()[df['User Type'].isna()].count()#; print("df['User Type'].isna()[df['User Type'].isna()].count() = ", nan_count)
    # Print result statement
    print("\n | See travels by user type.")
    # ... for all user types, incl. count and percentage
    for user_type, count in df['User Type'].value_counts().iteritems():
        print(" |  {} : {} [{}%]".format(user_type, count, round(count/total_count*100, 1)))
    # ... and for NaN values, incl. count and percentage
    print(" |  n/a : {} [{}%]\n".format(nan_count, round(nan_count/total_count*100, 1)))

    # TO DO: Display counts of gender
    try:
        #print("\ndf['Gender'].value_counts() = \n", df['Gender'].value_counts())
        # Check column for existing values
        value_count = df['Gender'].count()#; print("df['Gender'].count() = ", value_count)
        nan_count = df['Gender'].isna()[df['Gender'].isna()].count()#; print("df['Gender'].isna()[df['Gender'].isna()].count() = ", nan_count)
        # Print result statement...
        print("\n | See travels by gender.")
        # ... for all genders, incl. count and percentage
        for gender, count in df['Gender'].value_counts().iteritems():
            print(" |  {} : {} [{}%]".format(gender, count, round(count/total_count*100, 1)))
        # ... and for NaN values, incl. count and percentage
        print(" |  n/a : {} [{}%]\n".format(nan_count, round(nan_count/total_count*100, 1)))
    except:
        # Print except statement
        print(" | Based on the selection, there is no gender data available!")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        # print("\ndf['Birth Year'].value_counts() = \n", df['Birth Year'].value_counts())
        # Check column for existing values
        value_count = df['Birth Year'].count()#; print("df['Birth Year'].count() = ", value_count)
        nan_count = df['Birth Year'].isna()[df['Birth Year'].isna()].count()#; print("df['Birth Year'].isna()[df['Birth Year'].isna()].count() = ", nan_count)
        # Get first, last and most frequent value, incl. count
        first = int(df['Birth Year'].min())
        last = int(df['Birth Year'].max())
        top = int(df['Birth Year'].mode()[0])
        count_first = df['Birth Year'].value_counts()[first]
        count_last = df['Birth Year'].value_counts()[last]
        count_top = df['Birth Year'].value_counts()[top]
        # Print result statement
        print("\n | See travels by year of birth.")
        print(" |  Most customers were born in {} : {} [{}%]".format(top, count_top, round(count_top/total_count*100, 1)))
        print(" |  Our youngest customers were born in {} : {} [{}%]".format(last, count_last, round(count_last/total_count*100, 1)))
        print(" |  Our customers with the most life experienece were born in {} : {} [{}%]".format(first, count_first, round(count_first/total_count*100, 1)))
    except:
        # Print except statement
        print(" | Based on the selection, there is no birth year data available!")

    ###
    #print("\ndf = \n", df[['City', 'User Type', 'Gender', 'Birth Year']])#, 'Gender', 'Birth Year'])
    ###

    # Print a general reminder
    print("\n | Please keep in mind: gender and birth year data is not available for the city of Washington at the moment.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def show_raw_data(df):
    """
    Asks for the interest in raw data and displays the selected number of lines of raw data.

    Args:
        df - Pandas DataFrame containing city data filtered by month, week and/or weekday

    Returns:
        n/a

    """
    # Create line counter, from incl., to excl., and max available lines
    line_from = 0
    line_to = 0
    line_max = df.shape[0]

    # Ask for user input if / how many lines of raw data
    while True:
        lines = input("\nWould you like to see some additional raw data?\n | Based on your selection, there are {} lines of raw data in total. Just type in the number of lines you would like to see.\n | Or hit Enter without any input to move on.\n\n Please enter your selection: ".format(line_max))
        # Check if the input is an integer
        try:
            lines = int(lines)
        # Let management users jump real quick and without much effort out of a situation with too much detail
        except:
            break

        # Handle funny poeple
        if lines == 0:
            print("\nAlright, sure, you'll get to see 0 lines of raw data.")
            break # Actually this is a valid way to express the lack of interest in raw data :)
        if lines < 0:
            lines = (-1)*lines
            print("\nYou typed in a negative number. Must have been accidentally.\nBut no problem, you'll get to see {} lines of raw data instead!".format(lines))

        # Display rows from line_from to line_to until line_max
        line_to +=lines
        # Handle the line_max situation
        if line_to > line_max:
            print("\nSince your selection exceeded the available lines of raw data, you'll get to see the last available {} lines :".format(line_max-line_from))
            # Print the raw data
            print(df[line_from:line_max])
            print("\nThere is no more raw data available based on your selection.\n")
            break
        # Make the selection of rows, eg. 0-3excl. look like an expected outcome for the user, eg. 1-3
        print("\nFeel free to have a look at the lines {}-{} / {} from the Divvy raw data below :".format(line_from+1, line_to, line_max))
        # Print the raw data
        print(df[line_from:line_to])
        line_from +=lines
        line_to = line_from
        # Check if line_max was reached
        if line_to == line_max:
            print("\nThere is no more raw data available based on your selection.\n")
            break



def main():

    while True:
        city, month, week, day = get_filters()
        df = load_data(city, month, week, day)

        # Check if data was loaded
        if not df.empty:

            # Run statistic functions
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            # Run raw data functions
            show_raw_data(df)

            # Check that a random doc_string works
            # print ("What the load_data function does: \n", load_data.__doc__)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if (restart.lower() != 'yes') and (restart.lower() != 'y'):
            break

        # Reference GitHub


if __name__ == "__main__":
	main()
