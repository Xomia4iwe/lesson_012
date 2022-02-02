import threading

import csv
import math
import zipfile


class ParseFile(threading.Thread):
    def __init__(self, name_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_file = name_file
        self.volatility_ticker = None
        self.name_ticker = None
        self.zip = None

    def run(self):
        with open(self.name_file) as File:
            reader = csv.reader(File)
            max_price_ticker, min_price_ticker = self.search_max_min_ticker(reader)
        half_sum_ticker = (max_price_ticker + min_price_ticker) / 2
        volatility_ticker = ((max_price_ticker - min_price_ticker) / half_sum_ticker) * 100

        self.volatility_ticker = volatility_ticker

    def search_max_min_ticker(self, reader):
        max_price_ticker = -math.inf
        min_price_ticker = math.inf
        for row in reader:
            if row == ['SECID', 'TRADETIME', 'PRICE', 'QUANTITY']:
                continue
            self.name_ticker = row[0]
            max_price_ticker = max(max_price_ticker, float(row[2]))
            min_price_ticker = min(min_price_ticker, float(row[2]))
        return max_price_ticker, min_price_ticker


class ExtractZiFile:
    def __init__(self, file_zip_path_downloaded):
        self.file_zip_path_downloaded = file_zip_path_downloaded
        self.names_file = []

    def extract_zip_file(self):
        self.checking_name_file()
        for name_file in self.zip.namelist():
            self.zip.extract(member=name_file)
            if name_file[-4:] == '.csv':
                self.names_file.append(name_file)

    def checking_name_file(self):
        try:
            self.zip = zipfile.ZipFile(file=self.file_zip_path_downloaded, mode='r')
        except Exception as e:
            print(e)


file_zip_path_downloaded = 'trades.zip'
zip_open = ExtractZiFile(file_zip_path_downloaded=file_zip_path_downloaded)
zip_open.extract_zip_file()


class Manager:
    def __init__(self, names_file):
        self.names_file = names_file
        self.date = []
        self.date_volatility_ticker_0 = []

    def main(self):
        parsers = [ParseFile(name) for name in self.names_file]
        for parser in parsers:
            parser.start()
        for parser in parsers:
            parser.join()
            if parser.volatility_ticker == 0:
                self.date_volatility_ticker_0.append(parser.name_ticker)
            else:
                self.date.append([parser.name_ticker, parser.volatility_ticker])
        self.ssort()
        self.pprint()

    def ssort(self):
        self.date.sort(key=lambda x: x[1], reverse=True)
        self.date_volatility_ticker_0.sort()

    def pprint(self):

        print('Максимальная волатильность:')
        for line in self.date[:3]:
            print(f'{line[0]} - {round(line[1], 2)} %')

        print('\nМинимальная волатильность:')
        for line in self.date[-3:]:
            print(f'{line[0]} - {round(line[1], 2)} %')

        print('\nНулевая волатильность:')
        for line in self.date_volatility_ticker_0:
            if line != self.date_volatility_ticker_0[-1]:
                print(f'{line}', end=', ')
            else:
                print(f'{line}')


A = Manager(zip_open.names_file)
A.main()