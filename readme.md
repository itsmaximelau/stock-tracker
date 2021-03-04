## Description
Command-line interface stock tracker to get basic stock informations (watchlist) and create/track your portfolio.

## What have I learned ?
- Web scraping (with BeautifulSoup)
- CLI formatting
- SQLite3

## How does it work ?
This program works in a command-line interface. 

WATCHLIST :
User has the choice to input stock ticker in his watchlist to keep track of the stock price. 

PORTFOLIO :
User has the choice to input transactions to keep track of his portfolio value in real-time.

STOCK TRACKER : 
Once tickers and/or transactions has been input, user can launch live stock tracker. Then, the program scrapes data from Yahoo! Finance to give real-time data according to user input. Data refreshes every 45 seconds (editable).

## Example

```
WATCHLIST
+--------+---------------+----------------------+--------------------+--------------------+
| Ticker | Current price | Previous close price | Daily variance ($) | Daily variance (%) |
+--------+---------------+----------------------+--------------------+--------------------+
|  SPY   |    $381.42    |       $386.54        |       -$5.12       |       -1.32%       |
|  GME   |    $124.18    |       $118.18        |       $6.00        |       5.08%        |
|  MSFT  |    $227.56    |       $233.87        |       -$6.31       |       -2.70%       |
|  NIO   |     $41.53    |        $43.29        |       -$1.76       |       -4.07%       |
+--------+---------------+----------------------+--------------------+--------------------+

PORTFOLIO
+--------+---------------+---------------+---------------+---------------+
| Ticker | Daily P/L ($) | Daily P/L (%) | Total P/L ($) | Total P/L (%) |
+--------+---------------+---------------+---------------+---------------+
|  TSLA  |     -664.8    |     -5.09     |     3064.0    |     30.64     |
|  GME   |     300.0     |      4.83     |     4209.0    |     210.45    |
+--------+---------------+---------------+---------------+---------------+

Last refresh : 09:27:27
```

## Setup
To run this project, you must install requirements stated in requirements.txt file, which are the following :
- console_menu==0.6.0
- prettytable==2.0.0
- beautifulsoup4==4.9.3
- consolemenu==1.0.1

Once requirements are installed, you can simply run main.py and use the program through the CLI menu.

## To do
I plan on adding the following features :
- Get portfolio total
- Set a different currency
- Add cash balance
