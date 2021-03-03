import os
import time
from urllib.request import urlopen
import yahoo_finance_query
from prettytable import PrettyTable
import sqlite3
from pathlib import Path
import cli

class DetainedStock:
    def __init__(self,ticker,db) -> None:
        self.quantity, self.book_net_price = db.get_portfolio_stock_summary(ticker)

class StockPortfolioData:
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
        
        try:
            self.day_variance_percentage_portfolio = round((self.day_variance_portfolio/self.current_total_value)*100,2)
        
        except:
            self.day_variance_percentage_portfolio = 0

        self.total_variance_portfolio = round(self.current_total_value - self.book_total_cost,2)
        
        try:
            self.total_variance_percentage_portfolio = round((self.total_variance_portfolio/self.book_total_cost)*100,2)

        except:
            self.total_variance_percentage_portfolio = 0

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
        
        data_folder = Path("data")
        database = data_folder / str(name+".sqlite")
        
        if not os.path.isfile(str(database)):
            self.conn = sqlite3.connect(str(database),check_same_thread=False)
            self.c = self.conn.cursor()
            self.c.execute('''CREATE TABLE portfolio
                ([id] INTEGER PRIMARY KEY, [trans_type] text, [Ticker] text, [Date] text, [Quantity] integer,[Currency] text,[BookPrice] float, [brokerage_fee] float, [net_price] float)''')
            self.c.execute('''CREATE TABLE watchlist
                ([id] INTEGER PRIMARY KEY, [Ticker] text)''')
            self.conn.commit()
        else:
            self.conn = sqlite3.connect(str(database),check_same_thread=False)
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
        sql = '''INSERT INTO portfolio (trans_type, Ticker, Date, Quantity, Currency, BookPrice, brokerage_fee, net_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
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
    
    def get_portfolio_transaction_id(self,id):
        sql = '''SELECT * FROM  portfolio WHERE id=(?)'''
        data = self.fetchall_database(sql, [id])
        return data
    
    def get_watchlist_ticker_entry(self,ticker):
        sql = '''SELECT * FROM  watchlist WHERE ticker=(?)'''
        data = self.fetchall_database(sql, [ticker])
        return data
    
    def get_portfolio_tickers(self):
        sql = '''SELECT DISTINCT Ticker FROM portfolio'''
        data = self.fetchall_database(sql)
        
        ticker_list = []
        
        for ticker in data:
            ticker_list.append(ticker[0])
   
        return ticker_list 
    
    def get_portfolio_stock_summary(self,ticker): 
        sql = '''SELECT Ticker, SUM(Quantity), SUM(net_price) FROM portfolio WHERE Ticker = (?) GROUP BY Ticker'''
        data = self.fetchall_database(sql, [ticker])
        
        try:
            quantity = data[0][1]
        
        except:
            quantity = 0
        
        try:
            net_price = data[0][2]
        
        except:
            net_price = 0
           
        return quantity, net_price

    def delete_in_database_portfolio(self,entry):
        sql = '''DELETE FROM portfolio WHERE id= (?);'''
        self.execute_database(sql,[entry])

    def delete_in_database_watchlist(self,entry):
        sql = '''DELETE FROM watchlist WHERE ticker= (?);'''
        self.execute_database(sql,[entry])

    def choosePortfolioCurrencyDisplay():
        pass

    def deleteFromDatabase():
        pass

class Tracker:
    def __init__(self,refresh,db) -> None:
        self.refresh = refresh
        self.db = db

    def launch_tracker(self):
        while(True):
            # Portfolio
            tickers = Database.get_portfolio_tickers(self.db)
            portfolio_tickers_dict = {}
            for ticker in tickers:
                portfolio_data = StockPortfolioData(ticker,self.db)
                data_dict = {
                    ticker : {
                        "day_variance_portfolio" : portfolio_data.day_variance_portfolio,
                        "day_variance_percentage_portfolio" : portfolio_data.day_variance_percentage_portfolio,
                        "total_variance_portfolio" : portfolio_data.total_variance_portfolio,
                        "total_variance_percentage_portfolio" : portfolio_data.total_variance_percentage_portfolio
                    }
                }
                portfolio_tickers_dict.update(data_dict)
        
            # Watchlist    
            tickers = Database.get_watchlist_tickers(self.db)
            watchlist_tickers_dict = {}
            for ticker in tickers:
                watchlist_data = StockPortfolioData(ticker,self.db)
                data_dict = {
                    ticker : {
                        "current_price" : watchlist_data.price,
                        "previous_close_price" : watchlist_data.previous_close_price,
                        "day_variance" : watchlist_data.day_variance_stock,
                        "day_variance_percent" : watchlist_data.day_variance_percentage_stock
                    }
                }
                watchlist_tickers_dict.update(data_dict)

            cli.print_watchlist_data(watchlist_tickers_dict)
            cli.print_portfolio_data(portfolio_tickers_dict)
            cli.print_current_time()

            # Refresh rate
            time.sleep(self.refresh)
            
            # Refresh interface
            os.system('cls' if os.name == 'nt' else 'clear')