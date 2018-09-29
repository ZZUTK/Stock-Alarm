# load stock data
from collections import OrderedDict
import csv


class Stocks(object):
    def __init__(self, stock_file='./stocks.csv'):
        """
        :param stock_file: str, a CSV file
        """
        self.stock_file = stock_file
        self.stocks = self.read_csv_file()

    def read_csv_file(self):
        stocks = {}

        def check_number(s):
            s = s.strip()
            try:
                s = float(s)
                return s
            except ValueError:
                return s

        with open(self.stock_file, 'rb') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                ticker = row['ticker'].strip()
                stocks[ticker] = dict([(x[0].strip(), check_number(x[1])) for x in row.items()])

        return OrderedDict(sorted(stocks.items(), key=lambda x: x[0]))

    def check_modification(self):
        latest_stocks = self.read_csv_file()
        unmatched_tickers = []
        for ticker in self.stocks:
            if ticker in latest_stocks:
                for key in ['threshold', 'expectation']:
                    if self.stocks[ticker][key] != latest_stocks[ticker][key]:
                        unmatched_tickers.append((ticker, key))
                        self.stocks[ticker][key] = latest_stocks[ticker][key]
        return unmatched_tickers


if __name__ == '__main__':
    from time import sleep
    stock_dict = Stocks()
    current_stocks = stock_dict.stocks
    while True:
        for ticker in current_stocks:
            print ticker, current_stocks[ticker]
        m = stock_dict.check_modification()
        if m:
            for t in m:
                current_stocks[t[0]][t[1]] = stock_dict.stocks[t[0]][t[1]]
        sleep(5)
