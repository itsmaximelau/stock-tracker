import os
import time
from datetime import datetime
import bs4
from urllib.request import urlopen
import yahoo_finance_query
from prettytable import PrettyTable
import sqlite3

class DetainedStock:
    def __init__(self,ticker,db) -> None:
        self.quantity, self.book_net_price = db.get_portfolio_stock_summary(ticker)

class StockPortfolioData():
    def __init__(self,ticker,db) -> None:
        
        self.stock = yahoo_finance_query.Stock(ticker)
        self.detained_stock = DetainedStock(ticker,db)
        
        self.price = self.stock.current_price
        self.quantity = self.detained_stock.quantity
        self.book_net_price = self.detained_stock.book_net_price
        self.book_total_cost = round(self.quantity * self.book_net_price,2)
        self.current_total_value = round(self.quantity * self.price,2)
        
        self.previous_close_price = self.stock.previous_close_price
        self.day_variance_stock = round(self.price-self.previous_close_price,2)
        self.day_variance_percentage_stock = round((self.day_variance_stock/self.previous_close_price)*100,2)
        self.day_variance_portfolio = round(self.quantity * self.day_variance_stock,2)
        self.day_variance_percentage_portfolio = round((self.day_variance_portfolio/self.current_total_value)*100,2)

        self.total_variance_portfolio = round(self.current_total_value - self.book_total_cost,2)
        self.total_variance_percentage_portfolio = round((self.total_variance_portfolio/self.book_total_cost)*100,2)

class Portfolio:
    def __init__(self,database) -> None:
        self.database = database
        self.tickers = self.database.get_portfolio_tickers()
        
    def update_tickers(self):
        self.tickers = self.database.get_portfolio_tickers()

class Watchlist:
    def __init__(self,database) -> None:
        self.database = database
        self.tickers = self.database.get_watchlist_tickers()
        
    def update_tickers(self):
        self.tickers = self.database.get_watchlist_tickers()
        
class Database:
    def __init__(self,name) -> None:
        
        if not os.path.isfile(str(name+'.sqlite')):
            self.conn = sqlite3.connect(str(name+'.sqlite'),check_same_thread=False)
            self.c = self.conn.cursor()
            self.c.execute('''CREATE TABLE portfolio
                ([id] INTEGER PRIMARY KEY, [TransType] text, [Ticker] text, [Date] text, [Quantity] integer,[Currency] text,[BookPrice] float, [BrokerageFee] float, [NetPrice] float)''')
            self.c.execute('''CREATE TABLE watchlist
                ([id] INTEGER PRIMARY KEY, [Ticker] text)''')
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(str(name+'.sqlite'),check_same_thread=False)
            self.c = self.conn.cursor()

    def execute_database(self,sql,entry):
        self.c.execute(sql,entry)
        self.conn.commit()
        
    def fetchall_database(self,sql,entry=None):
        if entry is None:
            self.c.execute(sql)
        else :
            self.c.execute(sql,entry)
        return self.c.fetchall()
    
    def save_to_database_portfolio(self,entry):
        sql = '''INSERT INTO portfolio (TransType, Ticker, Date, Quantity, Currency, BookPrice, BrokerageFee, NetPrice) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        self.execute_database(sql,entry)
        
    def save_to_database_watchlist(self,entry):
        sql = '''INSERT INTO watchlist (Ticker) VALUES (?)'''
        self.execute_database(sql,[entry])
        
    def get_watchlist_tickers(self):
        sql = '''SELECT DISTINCT Ticker FROM watchlist'''
        data = self.fetchall_database(sql)
        
        ticker_list = []
        
        for ticker in data:
            ticker_list.append(ticker[0])
   
        return ticker_list 
    
    def get_portfolio_transactions(self):
        sql = '''SELECT * FROM  portfolio '''
        data = self.fetchall_database(sql)
        return data
    
    def get_portfolio_tickers(self):
        sql = '''SELECT DISTINCT Ticker FROM portfolio'''
        data = self.fetchall_database(sql)
        
        ticker_list = []
        
        for ticker in data:
            ticker_list.append(ticker[0])
   
        return ticker_list 
    
    def get_portfolio_stock_summary(self,ticker):
        
        sql = '''SELECT Ticker, SUM(Quantity), SUM(NetPrice) FROM portfolio WHERE Ticker = (?) GROUP BY Ticker'''
        data = self.fetchall_database(sql, [ticker])
        
        quantity = data[0][1]
        net_price = data[0][2]
        
        return quantity, net_price
    
    
    
    
    
    
    
    
    
    
    def viewTransactions():
        #print("No transactions found... Please add transactions before trying to view transactions. You will be redirected to main menu in 10 seconds.")

        transactions = fetchTransactions()

        for row in transactions:
            print(row)

        input("Press any key to go back to main menu.")

    def deleteTransaction():
        pass

    def choosePortfolioCurrencyDisplay():
        pass

    def deleteFromDatabase():
        pass
    

def launch_tracker():
    pass
    
        
        

"""
def launchTracker():
    while(True):
        # Portfolio
        tickers = Portfolio.get_tickers_in_portfolio()
        portfolio_tickers_dict = {}
        for ticker in tickers:
            data = mergeStockData(ticker)
            data_dict = {
                ticker : {
                    "dayVariancePortfolio" : data["dayVariancePortfolio"],
                    "dayVariancePercentagePortfolio" : data["dayVariancePercentagePortfolio"],
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
        time.sleep(40)
        
        # Refresh interface
        os.system('cls' if os.name == 'nt' else 'clear')
"""