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
 ![Example](https://raw.githubusercontent.com/itsmaximelau/stock-tracker/master/resources/images/example1.png)

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
