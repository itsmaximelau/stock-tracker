import datetime
from prettytable import PrettyTable

def print_portfolio_data(data):    
    print("PORTFOLIO")
    main_table = PrettyTable(["Ticker","Daily P/L ($)","Daily P/L (%)","Total P/L ($)","Total P/L (%)"])
    
    for ticker in data:
        main_table.add_row([ticker,data[ticker]["dayVariancePortfolio"],data[ticker]["dayVariancePercentagePortfolio"],data[ticker]["totalVariancePortfolio"],data[ticker]["totalVariancePercentagePortfolio"]])

    print(main_table)
    print()
    
def print_watchlist_data(data):
    print()
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

def print_current_time():
    print("Last refresh : " + datetime.datetime.now().strftime("%H:%M:%S"))
    
def format_percentage(data):
    return "{:.2f}%".format(float(data))

def format_currency(data):
    if data < 0:
        data = "-${:.2f}".format(abs(data))
    else:
        data = "${:.2f}".format(data)
    return data

def add_transaction(database, portfolio):
    entry_added = False

    # Begining of loop until end of entry
    while not entry_added:
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

        # Net price calculation
        netPrice = float(price) + float(brokerageFee)
        
        # Validation completed at this point

        # Save entry
        transaction = (str(transType), str(ticker), str(date), int(quantity), str(currency), float(price), float(brokerageFee), float(netPrice)) 
        database.save_to_database_portfolio(transaction)
        
        portfolio.update_tickers()
        

        #End loop
        entry_added = True

def delete_transaction(database,portfolio):
    entry_deleted = False

    # Begining of loop until end of delete
    while not entry_deleted:
        # Transaction type
        entry_delete_id = entry_delete(database)

        # Delete entry
        database.delete_in_database_portfolio(entry_delete_id)
        
        portfolio.update_tickers()
        
        #End loop
        entry_deleted = True

def add_to_watchlist(database, watchlist):
    entry_added = False

    # Begining of loop until end of entry
    while not entry_added:
        
        # Stock ticker
        ticker = stockTickerInput()

        # Validation completed at this point

        # Save entry
        database.save_to_database_watchlist(ticker)
        
        watchlist.update_tickers()
        
        #End loop
        entry_added = True

def delete_from_watchlist(database,watchlist):
    entry_deleted = False

    # Begining of loop until end of delete
    while not entry_deleted:
        # Transaction type
        ticker = ticker_delete(database)

        # Delete entry
        database.delete_in_database_watchlist(ticker)
        
        watchlist.update_tickers()
        
        #End loop
        entry_deleted = True    

def view_transactions(database):
    user_input= False

    # Begining of loop until user input
    while not user_input:
        print("TRANSACTIONS")
        main_table = PrettyTable(["Id","Trans. type","Ticker","Date","Quantity","Currency","Book Price", "Brokerage fee", "Net price"])
        
        for ticker in database.get_portfolio_transactions():
            main_table.add_row([ticker[0],ticker[1],ticker[2],ticker[3],ticker[4],ticker[5],format_currency(ticker[6]),format_currency(ticker[7]),format_currency(ticker[8])])
        
        print(main_table)
        input("Press any key to go back to main menu.")
        user_input = True

def view_watchlist_tickers(database):
    user_input= False

    # Begining of loop until user input
    while not user_input:
        print("WATCHLIST")
        main_table = PrettyTable(["Ticker"])

        for ticker in database.get_watchlist_tickers():
            main_table.add_row([ticker])
        
        print(main_table)
        input("Press any key to go back to main menu.")
        user_input = True

def choose_portfolio_currency_display(database):
    pass
    
def addToWatchList():
    # Stock ticker
    ticker = stockTickerInput()
    # Save entry
    stockInformations = (ticker)
    saveToDatabaseWatchList([stockInformations])

def entry_delete(db):
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            id = input("Enter transaction id : ")
            entry_delete_validation(id,db)
            inputIncomplete = False
            return id

        except ValueError as reason:
            print(reason)
            
def ticker_delete(db):
    inputIncomplete = True
    while inputIncomplete == True:
        try:
            ticker = input("Enter ticker to delete : ")
            ticker_delete_validation(ticker,db)
            inputIncomplete = False
            return ticker

        except ValueError as reason:
            print(reason)

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
    
def entry_delete_validation(id,db):
    if len(db.get_portfolio_transaction_id(id)) == 0:
        raise ValueError("Error - Please select a valid transaction ID.")
    
def ticker_delete_validation(ticker,db):
    if len(db.get_watchlist_ticker_entry(ticker)) == 0:
        raise ValueError("Error - Please select a valid ticker.")