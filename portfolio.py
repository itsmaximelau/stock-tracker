from consolemenu import *
from consolemenu.items import *
import os
import sqlite3
import datetime

def addTransaction():
    if not os.path.isfile("portfolio.sqlite"):
        createDatebase()

    entryAdded = False

    # Begining of loop until end of entry
    while not entryAdded:
        # Stock ticker
        ticker = stockTickerInput()

        # Transaction date
        date = transactionDateInput()
        
        # Stock currency
        currency = stockCurrencyInput()

        # Stock price
        price = stockPriceInput()
        
        # Validation completed at this point

        # Save entry
        stockInformations = (ticker, currency, price)
        saveToDatabase(stockInformations)

        #End loop
        entryAdded = True
        
def deleteTransaction():
    pass

def choosePortfolioCurrencyDisplay():
    pass

def saveToDatabase(entry):
    conn = sqlite3.connect('portfolio.sqlite')
    sql = '''INSERT INTO portfolio (Ticker, Currency, BookPrice) VALUES (?, ?, ?)'''
    c = conn.cursor()
    c.execute(sql, entry)
    conn.commit()

def deleteFromFile():
    pass

def stockTickerInput():
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            ticker = input("Enter stock ticker : ")
            stockTickerValidation(ticker)
            inputIncomplete = False
            return ticker

        except ValueError as reason:
            print(reason)

def transactionDateInput():
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            date_entry = input('Enter a date in YYYY-MM-DD format : ')
            year, month, day = map(int, date_entry.split('-'))
            date = datetime.date(year, month, day)
            inputIncomplete = False
            return date

        except ValueError:
            print("Wrong date")

def stockCurrencyInput():
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            currency = input("Enter stock currency (CAD = 1 and USD = 2) : ")
            stockCurrencyValidation(currency)
            inputIncomplete = False
            return currency

        except ValueError as reason:
            print(reason)

def stockPriceInput():
    inputIncomplete = True
    while inputIncomplete == True:    
        try:
            price = input("Enter stock book value (price you paid per unit) : ")
            stockPriceValidation(price)
            inputIncomplete = False
            return price

        except ValueError as reason:
            print(reason)

def stockTickerValidation(ticker):
    if not (3 <= len(ticker) <= 4):
        print(str("Ticker you entered "+"("+ ticker +") does not respect the convetional naming convention. \n Are you sure you correctly entered the ticker ? If ticker is incorrect, stock data wont be retrieved."))
        correctTicker = input("Continue with current ticker (y/n)")
        if correctTicker == "n":
            raise ValueError("Error - Please enter a new ticker.")

def stockCurrencyValidation(currency):
    if currency == str(1):
        return "CAD"

    elif currency == str(2):
        return "USD"

    else:
        raise ValueError("Error - Please select a valid currency (1 for CAD, 2 for USD). Other currencies are not supported yet.")

def stockPriceValidation(price):
    if float(price) < 0:
        raise ValueError("Error - Please select a valid price (must be greater than 0).")

def viewTransactions(): 
    pass

def choosePortfolioCurrencyDisplay():
    pass

def launchStockTracker():
    pass

def createDatebase():
    conn = sqlite3.connect('portfolio.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE portfolio
             ([generated_id] INTEGER PRIMARY KEY,[Ticker] text, [Quantity] integer,[Currency] integer,[BookPrice] float, [MarketPrice] float, [Variance] float)''')
    conn.commit()

### CLI MENU ###
menu = ConsoleMenu("Stock Tracker & Portfolio Manager")

#Portfolio
addTransaction = FunctionItem("Add a transaction", addTransaction)
deleteTransaction = FunctionItem("Delete a transaction", deleteTransaction)
viewTransactions = FunctionItem("View transactions", viewTransactions)
choosePortfolioCurrencyDisplay = FunctionItem("Choose portfolio currency displayed", choosePortfolioCurrencyDisplay)

#Stock tracker
launchStockTracker = FunctionItem("Launch live stock tracker", launchStockTracker)

menu.append_item(addTransaction)
menu.append_item(deleteTransaction)
menu.append_item(viewTransactions)
menu.append_item(choosePortfolioCurrencyDisplay)
menu.append_item(launchStockTracker)

menu.show()
