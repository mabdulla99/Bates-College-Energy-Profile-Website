import pandas as pd
import numpy as np

def cleaner(file):

    """
    :param file: file to be cleaned
    :return: cleaned pandas dataframe that may be saved to database.

    """

    #  dictionary for tolerance of each building's energy value

    tolerances_dict = {'Adams': 50, 'Bertram': 50, 'Carnegie': 800, 'Chapel': 20, 'Chase': 300, 'Pettigrew': 100,
                       'Rzasa': 100, 'Libbey': 50, 'Page': 50, 'Rand': 50, 'Schaeffer': 50, 'Lane': 300,
                       'Ladd': 300, 'Hathorn': 50, 'Parker': 50, 'Cheney': 50, 'Dana': 300, 'Underhill': 1000,
                       'Underhill Ice': 1000, 'Olin': 200, 'Pettengill': 400}

    df = pd.read_csv(file)

    #  renaming columns to remove kW notation

    subs = {}

    for column in df:
        best_guess = column.split(' (')[0]

        if best_guess == 'UnderhillIce':
            best_guess = 'Underhill Ice'

        elif best_guess == 'LaddLibrary':
            best_guess = 'Ladd'

        elif best_guess == 'Rsasa':
            best_guess = 'Rzasa'

        subs[column] = best_guess

    df.rename(columns=subs, inplace=True)

    #  removing out of tolerance values and converting NaNs to np.nan

    for index, row in df.iterrows():
        for column in df.columns[1:]:
            if not 0 <= df.at[index, column] < tolerances_dict[column] or np.isnan(df.at[index, column]) == True:
                df.at[index, column] = np.nan

    #  extrapolating NaN values

    for column in df.columns[1:]:
        for index, rows in df.iterrows():

            if np.isnan(df.at[index, column]):
                j = index + 1

                while j < len(df):
                    if np.isnan(df.at[j, column]):
                        j = j + 1

                    elif np.isnan(df.at[j, column]) != True and index != 0:
                        df.at[index, column] = round(np.average([df.at[index - 1, column], df.at[j, column]]), 1)
                        break

                    #  only for the case where the very first value of a column is a NaN

                    elif np.isnan(df.at[j, column]) != True and index == 0:
                        df.at[index, column] = round(np.average([df.at[j, column] for j in range(j, j + 10)]), 1)
                        break

    df = df.set_index('timestamp')
    df.index = pd.to_datetime(df.index, errors='ignore', utc=True)

    return df