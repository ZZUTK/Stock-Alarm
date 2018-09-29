# Stock-Alarm
An alarm for stock price. When the price of a stock is lower than or equal to certian threshold, you will get alert by email.

***Warning: Do NOT distribute the script because the alert email is sent via a Gmail account, whose password is in the code.***

## Pre-requisites
* Python 2.7+

## TODO
Set your stocks in [`stocks.csv`](stocks.csv) by following the examples.

The headers in `stocks.csv`: 
* ticker - stock symbol
* name - stock name for your convenience
* threshold - the low price triggering alarm
* expectation - the high price triggering alarm

## Run
Tested on Windows 8.1 and CentOS 7 (Linux)
```
$ python stock_alarm.py --email xxx@xxx.xxx
```
Set the email to receive the alarm.

