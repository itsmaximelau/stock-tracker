import consolemenu as cm
import os
import sqlite3
import datetime

def addTransaction():
    entryAdded = False

    # Begining of loop until end of entry
    while not entryAdded:
        # Transaction type
        transType = transactionTypeInput()

        # Stock ticker
        ticker = stockTickerInput()

        # Transaction date
        date = transactionDateInput()

        # Stock quantity
        quantity = stockQuantityInput()
        
        # Stock currency
        currency = stockCurrencyInput()

        # Stock price
        price = stockPriceInput()

        # Brokerage Fee
        brokerageFee = brokerageFeeInput()

        # Validation completed at this point

        # Save entry
        stockInformations = (transType, ticker, date, quantity, currency, price, brokerageFee) 
        saveToDatabase(stockInformations)

        #End loop
        entryAdded = True

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

def saveToDatabase(entry):
    conn = sqlite3.connect('portfolio.sqlite')  
    sql = '''INSERT INTO portfolio (TransType, Ticker, Date, Quantity, Currency, BookPrice, BrokerageFee) VALUES (?, ?, ?, ?, ?, ?, ?)'''
    c = conn.cursor()
    c.execute(sql, entry)
    conn.commit()

def deleteFromDatabase():
    pass

def fetchTransactions(): 
    conn = sqlite3.connect('portfolio.sqlite')
    c = conn.cursor()
    c.execute('''SELECT * FROM  portfolio ''')
    rows = c.fetchall()
    return rows

def transactionTypeInput():
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            transType = input("Enter transaction type (Buy or Sell) : ")
            transactionTypeValidation(transType)
            inputIncomplete = False
            return transType

        except ValueError as reason:
            print(reason)

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
            datetime.date(year, month, day)
            inputIncomplete = False
            return date_entry

        except ValueError:
            print("Wrong date")

def stockQuantityInput():
    inputIncomplete = True
    while inputIncomplete == True:    
        try:
            quantity = input("Enter quantity bought : ")
            stockQuantityValidation(quantity)
            inputIncomplete = False
            return quantity

        except ValueError as reason:
            print(reason) 

def stockCurrencyInput():
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            currency = input("Enter stock currency (CAD or USD) : ")
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

def brokerageFeeInput():
    inputIncomplete = True
    while inputIncomplete == True:    
        try:
            brokerageFee = input("Enter the brokerage fee (broker commission - if none, enter 0) : ")
            brokerageFeeValidation(brokerageFee)
            inputIncomplete = False
            return brokerageFee

        except ValueError as reason:
            print(reason)

def transactionTypeValidation(transType):
    if transType.upper() == "BUY":
        return "Buy"

    elif transType.upper() == "SELL":
        return "Sell"

    else:
        raise ValueError("Error - Please select a valid transaction type (Buy or Sell)")

def stockTickerValidation(ticker):
    if not (3 <= len(ticker) <= 4):
        print(str("Ticker you entered "+"("+ ticker +") does not respect the convetional naming convention. \n Are you sure you correctly entered the ticker ? If ticker is incorrect, stock data wont be retrieved."))
        correctTicker = input("Continue with current ticker (y/n)")
        if correctTicker == "n":
            raise ValueError("Error - Please enter a new ticker.")

def stockCurrencyValidation(currency):
    if currency.upper() == "CAD":
        return "CAD"

    elif currency.upper() == "USD":
        return "USD"

    else:
        raise ValueError("Error - Please select a valid currency (CAD or USD). Other currencies are not supported yet.")

def stockQuantityValidation(quantity):
    try :
        if int(quantity) <= 0:
            raise ValueError("Error - Please select a valid quantity (must be greater than 0).")

    except ValueError:
        raise ValueError("Error - Please enter a valid quantity (must be greater than 0 and not be a string).")

def stockPriceValidation(price):
    if float(price) <= 0:
        raise ValueError("Error - Please select a valid price (must be greater than 0).")

def brokerageFeeValidation(brokerageFee):
    if float(brokerageFee) < 0:
        raise ValueError("Error - Please select a valid fee (must be greater or equal to 0).")

def launchStockTracker():
    pass

def createDatebase():
    conn = sqlite3.connect('portfolio.sqlite')
    c = conn.cursor()
    c.execute('''CREATE TABLE portfolio
             ([id] INTEGER PRIMARY KEY, [TransType] text, [Ticker] text, [Date] text, [Quantity] integer,[Currency] text,[BookPrice] float, [BrokerageFee] float)''')
    conn.commit()

# Create DB
if not os.path.isfile("portfolio.sqlite"):
    createDatebase()

### CLI MENU ###
menu = cm.ConsoleMenu("Stock Tracker & Portfolio Manager")

#Portfolio
addTransaction = cm.items.FunctionItem("Add a transaction", addTransaction)
deleteTransaction = cm.items.FunctionItem("Delete a transaction", deleteTransaction)
viewTransactions = cm.items.FunctionItem("View transactions", viewTransactions)
choosePortfolioCurrencyDisplay = cm.items.FunctionItem("Choose portfolio currency displayed", choosePortfolioCurrencyDisplay)

#Stock tracker
launchStockTracker = cm.items.FunctionItem("Launch live stock tracker", launchStockTracker)

menu.append_item(addTransaction)
menu.append_item(deleteTransaction)
menu.append_item(viewTransactions)
menu.append_item(choosePortfolioCurrencyDisplay)
menu.append_item(launchStockTracker)

menu.show()


