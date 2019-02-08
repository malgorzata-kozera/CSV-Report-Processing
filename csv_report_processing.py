import pycountry
import pandas as pd
import sys

"""
find_code()

Function  which uses Pycountry library. 
This function takes as an argument the country subdivision name(state name),then it looks for
subdivision's country code(ISO 3166-2 2-two-letter country code). Next it looks for the matching country code
alpha-3 (three-letter cede).   
Returns code alpha-3.
"""


def find_code(city_name):

    try:
        code_2 = pycountry.subdivisions.lookup(city_name)
        code_3 = pycountry.countries.get(alpha_2=code_2.country_code)
        return code_3.alpha_3
    except LookupError:
        print(f'Sorry, could not find a code for {city_name}', file=sys.stderr)
        return 'XXX'


"""
open_csv()
This function takes as an argument name of the csv file. 
File should be located in the same directory as this python script.
Function tries to open csv file in UTF-8 encoding, if it fails it opens with UTF-16.
"""


def open_csv(csv_file):

    columns_names = ['Date', 'State Name', 'Impression', 'CRT']

    try:
        file = pd.read_csv(csv_file, encoding='UTF-8', names=columns_names)

    except UnicodeDecodeError:
        file = pd.read_csv(csv_file, encoding='UTF-16', names=columns_names)

    return file


"""
creating_csv_file()
Creates a csv file with transformed data.
"""


def creating_csv_file():

    try:

        name_csv = input('Please enter name of  your CSV file (including extension).\n'
                             'It should be located in the same directory as this python file\n')

        df = open_csv(name_csv)

        # converts argument to datetime.

        df['Date'] = pd.to_datetime(df['Date'])

        # creating a new column 'Country' with 3 letter country code for each state

        df['Country'] = df['State Name'].apply(find_code)

        # for all arguments in column 'CRT' uses strip() function, which deletes '%' sign.

        df['CRT'] = df['CRT'].map(lambda x: x.strip('%'))

        # converts all elements(num) (in CRT) to floating point numbers.
        # creates new column 'Clicks' - The product of 'impression' and 'CRT'.

        for num in df['CRT']:
            float_digit = float(num)
            df['CRT'].replace(num, float_digit, inplace=True)

        df['Clicks'] = round(df['Impression'] * (df['CRT'] / 100))

        # converts all elements (in 'Clicks') to integers. Next removes unnecessary columns.

        df['Clicks'] = df['Clicks'].astype(int)

        df.drop('CRT', 1, inplace=True)

        df.drop('State Name', 1, inplace=True)

        # Arranges a new database in the right order, group by date,country (sorts alphabetically)

        df = df[['Date', 'Country', 'Impression', 'Clicks']]

        grouped = df.groupby(['Date', 'Country'])
        df = grouped.agg(sum)
        df.sort_values(['Date', 'Country'], ascending=True)

        # saves converted data frame in new csv file
        try:

            df.to_csv(f'output_{name_csv}', header=False, encoding='utf-8', line_terminator='\n')
            print('New cvs file with your data has been created')

        except Exception as e:
            print(e, file=sys.stderr)
            print("\nCouldn't create an output file")

    except Exception as e:
        print('\nError occured:')
        print(e, file=sys.stderr)
        print("\nCouldn't create an output file")


creating_csv_file()
