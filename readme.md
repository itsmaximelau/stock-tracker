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
|  TSLA  |    $665.97    |       $701.81        |      -$35.84       |       -5.11%       |
|  NIO   |     $42.74    |        $44.76        |       -$2.02       |       -4.51%       |
|  BABA  |    $237.18    |       $233.34        |       $3.84        |       1.65%        |
|  SPY   |    $394.37    |       $397.26        |       -$2.89       |       -0.73%       |
|  MSFT  |    $232.28    |       $237.04        |       -$4.76       |       -2.01%       |
+--------+---------------+----------------------+--------------------+--------------------+

PORTFOLIO
+--------+---------------+---------------+---------------+---------------+
| Ticker | Daily P/L ($) | Daily P/L (%) | Total P/L ($) | Total P/L (%) |
+--------+---------------+---------------+---------------+---------------+
|   KO   |     -$1.06    |     -1.05%    |     $3.43     |     3.50%     |
|   FB   |     -$6.88    |     -0.61%    |    $537.41    |     90.82%    |
| ------ |     ------    |     ------    |     ------    |      ----     |
| Total  |     -$7.94    |     -0.64%    |    $540.84    |     78.41%    |
+--------+---------------+---------------+---------------+---------------+

Last refresh : 14:19:23
'''

## Setup
To run this project, you must install requirements stated in requirements.txt file, which are the following :
- console_menu
- prettytable
- beautifulsoup4
- consolemenu

Once requirements are installed, you can simply run main.py and use the program through the CLI menu.

## To do (features that could be added in the future)
- Output data in a different currency.
- Add cash balance.

## Issues (to fix)
- Portfolio total may have a small error when refreshing, as total refreshes after each ticker refreshes (and values changes each second during when market is live).