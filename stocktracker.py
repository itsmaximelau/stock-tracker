import bs4
import os
import time
from datetime import datetime
import bs4
from urllib.request import urlopen
import yahooFinanceQuery
import portfolio
from prettytable import PrettyTable

def getCurrentTime():
    return datetime.now().strftime("%H:%M:%S")

def printPortfolioData(data):
    print("PORTFOLIO")
    main_table = PrettyTable(["Ticker","Daily P/L ($)","Daily P/L (%)","Total P/L ($)","Total P/L (%)"])
    for ticker, ticker_values in data.items():
        
        dayVarianceStock = ticker_values["dayVarianceStock"]
        if dayVarianceStock < 0:
            dayVarianceStock = "-${:.2f}".format(abs(dayVarianceStock))
        else:
            dayVarianceStock = "${:.2f}".format(dayVarianceStock)
        
        dayVariancePercentageStock = "{:.2f}%".format(float(ticker_values["dayVariancePercentageStock"]))
        
        totalVariancePortfolio = ticker_values["totalVariancePortfolio"]
        if totalVariancePortfolio < 0:
            totalVariancePortfolio = "-${:.2f}".format(abs(totalVariancePortfolio))
        else:
            totalVariancePortfolio = "${:.2f}".format(totalVariancePortfolio)
        
        totalVariancePercentagePortfolio = "{:.2f}%".format(float(ticker_values["totalVariancePercentagePortfolio"]))
        
        #Print out table line
        main_table.add_row([ticker,dayVarianceStock,dayVariancePercentageStock,totalVariancePortfolio,totalVariancePercentagePortfolio])
             
    print(main_table)
    print()

def printWatchlistData(data):
    print("WATCHLIST")
    main_table = PrettyTable(["Ticker","Current price","Previous close price","Daily variance ($)","Daily variance (%)"])
    for ticker, ticker_values in data.items():
        current_price = ticker_values["current_price"]
        if current_price < 0:
            current_price = "-${:.2f}".format(abs(current_price))
        else:
            current_price = "${:.2f}".format(current_price)
        
        previous_close_price = ticker_values["previous_close_price"]
        if previous_close_price < 0:
            previous_close_price = "-${:.2f}".format(abs(previous_close_price))
        else:
            previous_close_price = "${:.2f}".format(previous_close_price)        
        
        day_variance = ticker_values["day_variance"]
        if day_variance < 0:
            day_variance = "-${:.2f}".format(abs(day_variance))
        else:
            day_variance = "${:.2f}".format(day_variance)              
        
        day_variance_percent = "{:.2f}%".format(float(ticker_values["day_variance_percent"]))
        
        main_table.add_row([ticker,current_price,previous_close_price,day_variance,day_variance_percent])
    print(main_table)
    print()
    
def mergeStockData(ticker):
    databaseData = portfolio.getPortfolioStockData(ticker)
    currentData = yahooFinanceQuery.getStockData(ticker)

    quantity = databaseData["quantity"]
    bookNetPrice = databaseData["netPrice"]
    price = currentData["current_price"]
    previousClosePrice = currentData["previous_close_price"]
    dayVarianceStock = round(previousClosePrice-price,2)
    dayVariancePercentageStock = str(round((dayVarianceStock/previousClosePrice)*100,2))
    dayVariancePortfolio = round(quantity * dayVarianceStock,2)
    dayVariancePercentagePortfolio = 0
    bookTotalCost = round(quantity * bookNetPrice,2)
    currentTotalValue = round(quantity * price,2)
    totalVariancePortfolio = round(currentTotalValue - bookTotalCost,2)
    totalVariancePercentagePortfolio = 0
    
    data = {
        "ticker" : ticker,
        "price" : price,
        "quantity" : quantity,
        "previousClosePrice" : previousClosePrice,
        "dayVarianceStock" : dayVarianceStock,
        "dayVariancePercentageStock" : dayVariancePercentageStock,
        "dayVariancePortfolio" : dayVariancePortfolio,
        "dayVariancePercentagePortfolio" : dayVariancePercentagePortfolio,
        "totalVariancePortfolio" : totalVariancePortfolio,
        "totalVariancePercentagePortfolio" : totalVariancePercentagePortfolio
    }

    return data

def launchTracker():
    while(True):
        # Portfolio
        tickers = portfolio.getTickersInPortfolio()
        portfolio_tickers_dict = {}
        for ticker in tickers:
            data = mergeStockData(ticker)
            data_dict = {
                ticker : {
                    "dayVarianceStock" : data["dayVarianceStock"],
                    "dayVariancePercentageStock" : data["dayVariancePercentageStock"],
                    "totalVariancePortfolio" : data["totalVariancePortfolio"],
                    "totalVariancePercentagePortfolio" : data["totalVariancePercentagePortfolio"]
                }
            }
            portfolio_tickers_dict.update(data_dict)
            
        # Watchlist    
        tickers = portfolio.getTickersInWatchlist()
        watchlist_tickers_dict = {}
        for ticker in tickers:
            data = yahooFinanceQuery.getStockData(ticker)
            data_dict = {
                ticker : {
                    "current_price" : data["current_price"],
                    "previous_close_price" : data["previous_close_price"],
                    "day_variance" : data["day_variance"],
                    "day_variance_percent" : data["day_variance_percent"]
                }
            }
            watchlist_tickers_dict.update(data_dict)

        printWatchlistData(watchlist_tickers_dict)
        printPortfolioData(portfolio_tickers_dict)
            
        # Current time
        print("Last refresh : " + getCurrentTime())
        
        # Refresh rate
        time.sleep(60)
        
        # Refresh interface
        os.system('cls' if os.name == 'nt' else 'clear')