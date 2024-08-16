import pandas as pd
import time
import math


# these are links to datasets of apps in the stores

GooglePlayCsv = 'Google-Playstore.csv'
AppleStoreCsv = 'appleAppData.csv'


# here we take a csv file, sort it by popularity, remove the duplicates
# and return a list of lists as a result to be able to work with the other functions:


def read_csv_as_list_remove_duple(data, app_name, rating_name) -> list:
    start = time.time()
    data = pd.read_csv(data)
    data = data.sort_values(by=rating_name, ascending=False)
    data = data.drop_duplicates(subset=app_name, keep='first')
    data_list = data.values.tolist()
    print(time.time()-start)
    return data_list

# this function will be used to read the needed stack of information from a list
# and count its size on different steps of research:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        return len(dataset)

# ---------------------------validation------------------------------------------------------------


# for this function we go by the app info and check the price. The function returns True if the app is free and None
# if not


def is_free(row, price_index):
    if row[price_index] == 0.0:
        return True

# main function is based on identifying non ascii characters using an ord() function


def is_english(row, name_index):
    non_ASCII = 0
    try:
        for letter in row[name_index]:
            if ord(letter) > 127:
                non_ASCII += 1
    except TypeError:
        return False
    if non_ASCII > 3:
        return False
    else:
        return True

# replacing non values with zeroes:


def filling_nan(row):
    for i, value in enumerate(row):
        if type(value) is float:
            if math.isnan(value):
                row[i] = 0
    return row

# the main function for validation


def data_cleaning(data, price_index, name_index):
    start = time.time()
    result = []
    for row in data:
        new_row = filling_nan(row)
        if is_free(new_row, price_index) and is_english(new_row, name_index):
            result.append(new_row)
    print(time.time()-start)
    return result

# ------------------------------------main functions-------------------------------------------------------------------


# creating a dictionary with [name_of_a_genre] = percentage of apps MADE in this genre:


def freq_table(data, index):
    percent_100 = 0
    freq = {}
    for row in data:
        percent_100 += 1
        criteria = row[index]
        if criteria in freq.keys():
            freq[criteria] += 1
        else:
            freq[criteria] = 1
    for key, value in freq.items():
        freq[key] = round(value * 100 / percent_100, 3)
    return freq

# sorting dictionary & creating a better view on the picture:


def display_table(data, index):
    table = freq_table(data, index)
    table_sorted = sorted(table.items(), key=lambda item: item[1], reverse=True)
    for entry in table_sorted:
        print(entry[0], ':', entry[1])

# main function for ios


def ios_main(ios_data):
    genre_index = 3
    review_index = -3
    unique_genres = freq_table(ios_data, genre_index).keys()
    result = {}
    for genre in unique_genres:
        total = 0
        len_genre = 0
        for app in ios_data:
            genre_app = app[genre_index]
            if genre_app == genre:
                total += float(app[review_index])
                len_genre += 1
        avg_ratings = total / len_genre
        result[genre] = avg_ratings
    table_sorted = sorted(result.items(), key=lambda item: item[1], reverse=True)
    for entry in table_sorted:
        print(entry[0], ':', entry[1])


if __name__ == '__main__':
    ios_csv = read_csv_as_list_remove_duple(AppleStoreCsv, 'App_Name', 'Reviews')
    ios_clean = data_cleaning(ios_csv, price_index=10, name_index=1)
    ios_main(ios_clean)

    google_csv = read_csv_as_list_remove_duple(GooglePlayCsv, 'App Name', 'Rating Count')
    google_clean = data_cleaning(google_csv, price_index=10, name_index=1)
    ios_main(google_clean)
