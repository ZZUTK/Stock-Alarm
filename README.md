# Stock-Alarm
An alarm for stock price. When the price of a stock is lower than or equal to certian threshold, you will get alert by email. In addition, when the price is higher than or equal to your expectation, an alarm email will be sent.

***Warning: Do NOT distribute the script because the alert email is sent via a Gmail account, whose password is in the code.***

## Pre-requisites
* Python 2.7+

## TODO
Set your stocks in [`stocks.csv`](stocks.csv) by following the examples.

The headers in `stocks.csv`: 
* `ticker` - stock symbol
* `name` - stock name for your convenience
* `threshold` - the low price triggering alarm
* `expectation` - the high price triggering alarm

## Run
The code has been tested on Windows 8.1 and CentOS 7 (Linux). 
```
$ python stock_alarm.py --email xxx@xxx.xxx
```
Set the email to receive the alarm. 
As running, you will see the prompt:
```
Company             Price     Alarm    Expect         Last Update
---------------------------------------------------------------------------
Apple              225.74    200.00    240.00     2018-09-29 18:58:05
Amazon            2003.00   1900.00   2200.00     2018-09-29 18:58:00
FaceBook           164.46    150.00    180.00     2018-09-29 18:58:05
Google            1207.08   1180.00   1250.00     2018-09-29 18:58:05
Nvidia             281.02    240.00    320.00     2018-09-29 18:58:05
Tesla              264.77    240.00    320.00     2018-09-29 18:58:00
```

The `Price` shows the latest stock price whose update time is denoted by `Last Update`. `Alarm` and `Expect` indicate the lower threshold and higher threshold for sending the alarm email. 

**Note**: The setting of `Alarm` and `Expect` can be modified in `stocks.csv` (`threshold` and `expectation`) without interruption.
However, adding and removing a stock requires restart. 
