from stocks import Stocks
import json
from time import sleep
import smtplib
from email.mime.text import MIMEText
import urllib
from datetime import datetime
from threading import Thread
from collections import OrderedDict


class StockAlarm(Thread):
    # store stock prices, {ticker: [company_name, current_price, threshold, time_stamp]}
    __price_table = OrderedDict()

    def __init__(self, ticker, threshold, expectation, email, name, alarm_price_interval=.5, price_update_interval=5):
        """
        :param ticker: str, e.g., GOOGLE, AAPL, etc.
        :param threshold: float, threshold to trigger the alarm
        :param expectation: float, expected price
        :param email: str, email address to receive the alert
        :param name: str, name of the stock, any name that you can recognize the stock
        :param alarm_price_interval: float, price interval of triggering alarm, default $0.50
        :param price_update_interval: float, time interval of price update, default 5sec
        """
        Thread.__init__(self)
        self.ticker = ticker
        self.email = email
        self.threshold = threshold
        self.expectation = expectation
        self.name = name
        self.alarm_price_interval = alarm_price_interval
        self.price_update_interval = price_update_interval
        self.is_active = True

        # check input arguments
        assert isinstance(self.ticker, str)
        assert isinstance(self.email, str)

        # add stock to price table
        if self.ticker not in StockAlarm.__price_table:
            StockAlarm.__price_table[self.ticker] = []

    def run(self):
        while self.is_active:
            data = StockAlarm.get_stock_price(ticker=self.ticker)
            if data:
                price = data[0][-1]
                StockAlarm.__price_table[self.ticker] = [
                    self.name,
                    price,
                    self.threshold,
                    self.expectation,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
                if 0 < price <= self.threshold:
                    self.threshold = price - self.alarm_price_interval
                    subject = '%s (%s) fell to $%.2f' % (self.name, self.ticker, price)
                    StockAlarm.send_email(to_addrs=self.email, subject=subject, content=StockAlarm.price_table())
                elif price >= self.expectation:
                    self.expectation = price + self.alarm_price_interval
                    subject = '%s (%s) rose to $%.2f' % (self.name, self.ticker, price)
                    StockAlarm.send_email(to_addrs=self.email, subject=subject, content=StockAlarm.price_table())

            sleep(self.price_update_interval)

    def stop(self):
        self.is_active = False

    @staticmethod
    def get_stock_price(ticker, interval='Latest'):
        """
        :param ticker: str, the stock ticker name
        :param interval: str, ['Latest', 'Intraday', 'Daily', 'Weekly', 'Monthly']
        :return: list, [(date_time, open_price, close_price)]
        """

        # pre defined intervals
        intervals = {
            'Latest': 'GLOBAL_QUOTE',
            'Intraday': 'TIME_SERIES_INTRADAY',
            'Daily': 'TIME_SERIES_DAILY',
            'Weekly': 'TIME_SERIES_WEEKLY',
            'Monthly': 'TIME_SERIES_MONTHLY'
        }

        # check input arguments
        assert isinstance(ticker, str)
        assert isinstance(interval, str)
        if interval not in intervals:
            raise Exception('INTERVAL must be in %s' % str(intervals.keys()))

        # personal key obtained from https://www.alphavantage.co/
        api_key = '67HCBBBVFYQM9LYZ'

        # construct the request
        url = 'https://www.alphavantage.co/query?' \
              'function=%s&' \
              'symbol=%s&' \
              'apikey=%s&' \
              'outputsize=compact&' \
              'datatype=json&' \
              'interval=1min&' % \
              (intervals[interval], ticker, api_key)

        # request data
        response_data = []
        try:
            fp = urllib.urlopen(url)
            data = fp.read().decode('utf8')
            if data:
                response_data = json.loads(data)
            fp.close()
        except ValueError:
            pass

        # target the price data
        price_data = []
        for key in response_data:
            if 'Meta Data' not in key:
                price_data = response_data[key]
                break

        time_stamp = []
        price_open = []
        price_close = []

        if interval == 'Latest':
            for key in price_data:
                if 'day' in key:
                    time_stamp.append(price_data[key])
                elif 'open' in key:
                    price_open.append(float(price_data[key]))
                elif 'price' in key:
                    price_close.append(float(price_data[key]))
        else:
            for date_time in price_data:
                time_stamp.append(date_time)
                for key in price_data[date_time]:
                    if 'open' in key:
                        price_open.append(float(price_data[date_time][key]))
                    elif 'close' in key:
                        price_close.append(float(price_data[date_time][key]))

        date_price = zip(time_stamp, price_open, price_close)
        date_price = sorted(date_price, key=lambda x: x[0], reverse=True)

        return date_price

    @staticmethod
    def send_email(to_addrs, subject=None, content=None):
        """
        :param subject: str, subject of the email
        :param content: str, content of the email
        :param to_addrs: str, email address of the receiver
        """

        # sender email and password
        my_address = 'stock.alarm.server@gmail.com'
        pwd = 'Stock_Alarm_Server'

        # prepare the message
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = 'Stock Alarm'
        msg['To'] = 'Stocker'

        # login to Gmail server and send the email
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(user=my_address, password=pwd)
        server.sendmail(from_addr=my_address, to_addrs=to_addrs, msg=msg.as_string())
        server.close()

    @staticmethod
    def price_table():
        """
        :return: str, ready for print or save, visualizing the price table
        """
        head = '{:<15}{:>10}{:>10}{:>10}{:^30}\n{:-<75}\n'.format('Company', 'Price', 'Alarm', 'Expect', 'Last Update', '')
        line_format = '{:<15}{:10.2f}{:10.2f}{:10.2f}{:^30}\n'
        lines = head
        for ticker in StockAlarm.__price_table:
            if StockAlarm.__price_table[ticker]:
                lines += line_format.format(
                    StockAlarm.__price_table[ticker][0],
                    StockAlarm.__price_table[ticker][1],
                    StockAlarm.__price_table[ticker][2],
                    StockAlarm.__price_table[ticker][3],
                    StockAlarm.__price_table[ticker][4]
                )
        return lines


if __name__ == '__main__':
    import os
    import argparse
    parser = argparse.ArgumentParser('stock_alarm')
    parser.add_argument('--email', help='email to receive the alarm', required=True)
    args = parser.parse_args()

    print('Querying your stocks ...')

    # start threads, each of which monitors one stock
    stock_alarms = []
    stock_dict = Stocks()
    for ticker in stock_dict.stocks:
        stock_alarms.append(StockAlarm(
            ticker=ticker,
            threshold=stock_dict.stocks[ticker]['threshold'],
            expectation=stock_dict.stocks[ticker]['expectation'],
            email=args.email,
            name=stock_dict.stocks[ticker]['name']
        ))
        stock_alarms[-1].start()

    try:
        lines_pre = StockAlarm.price_table()
        while True:
            # print the price table
            lines = StockAlarm.price_table()
            if lines != lines_pre:
                lines_pre = lines
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                print(lines)

            # check stocks.csv for updates on threshold and expectation
            modification = stock_dict.check_modification()
            if modification:
                for ticker, key in modification:
                    for stock_alarm in stock_alarms:
                        if stock_alarm.ticker == ticker:
                            exec 'stock_alarm.%s = stock_dict.stocks[ticker][key]' % key
                            break
            sleep(5)
    except KeyboardInterrupt:
        # stop all threads
        for stock_alarm in stock_alarms:
            stock_alarm.stop()
