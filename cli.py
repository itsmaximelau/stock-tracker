import datetime
from prettytable import PrettyTable

# Printing functions
def print_portfolio_data(data,total):    
    print("PORTFOLIO")
    main_table = PrettyTable(["Ticker","Daily P/L ($)","Daily P/L (%)","Total P/L ($)","Total P/L (%)"])
    
    for ticker in data:
        daily_pl = format_currency(data[ticker]["day_variance_portfolio"])
        daily_pl_percentage = format_percentage(data[ticker]["day_variance_percentage_portfolio"])
        total_pl = format_currency(data[ticker]["total_variance_portfolio"])
        total_pl_percentage = format_percentage(data[ticker]["total_variance_percentage_portfolio"])

        main_table.add_row([ticker,daily_pl,daily_pl_percentage,total_pl,total_pl_percentage]) 
        
    total_daily_pl = 0
    total_daily_pl_percentage = 0
    total_total_pl = 0
    total_total_pl_percentage = 0
    
    total_daily_pl = format_currency(total["Total"]["total_daily_pl"])
    total_daily_pl_percentage = format_percentage(total["Total"]["total_daily_pl_percentage"])
    total_total_pl = format_currency(total["Total"]["total_total_pl"])
    total_total_pl_percentage = format_percentage(total["Total"]["total_total_pl_percentage"])
    
    main_table.add_row(["------","------","------","------","----"])
    main_table.add_row(["Total",total_daily_pl,total_daily_pl_percentage,total_total_pl,total_total_pl_percentage])
    
    print(main_table)
    print()
    
def print_watchlist_data(data):
    print()
    print("WATCHLIST")
    main_table = PrettyTable(["Ticker","Current price","Previous close price","Daily variance ($)","Daily variance (%)"])
    for ticker, ticker_values in data.items():
        current_price = format_currency(ticker_values["current_price"])
        previous_close_price = format_currency(ticker_values["previous_close_price"])
        day_variance = format_currency(ticker_values["day_variance"])
        day_variance_percent = format_percentage(ticker_values["day_variance_percent"])
        
        main_table.add_row([ticker,current_price,previous_close_price,day_variance,day_variance_percent])
    print(main_table)
    print()

def print_current_time():
    print("Last refresh : " + datetime.datetime.now().strftime("%H:%M:%S"))

# Formating
def format_percentage(data):
    return "{:.2f}%".format(float(data))

def format_currency(data):
    if data < 0:
        data = "-${:.2f}".format(abs(data))
    else:
        data = "${:.2f}".format(data)
    return data

# Input group functions
def add_transaction(database, portfolio):
    entry_added = False

    # Begining of loop until end of entry
    while not entry_added:
        # Transaction type
        trans_type = transaction_type_input()

        # Stock ticker
        ticker = stock_ticker_input()

        # Transaction date
        date = transaction_date_input()

        # Stock quantity
        quantity = stock_quantity_input()
        
        # Stock currency
        currency = stock_currency_input()

        # Stock price
        price = stock_price_input()

        # Brokerage Fee
        brokerage_fee = brokerage_fee_input()

        # Net price calculation
        net_price = float(price) + float(float(brokerage_fee)/int(quantity))
        
        # Validation completed at this point

        # Save entry
        transaction = (str(trans_type), str(ticker), str(date), int(quantity), str(currency), float(price), float(brokerage_fee), float(net_price)) 
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
        ticker = stock_ticker_input()

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
    
def entry_delete(db):
    input_incomplete = True
    while input_incomplete == True:
        try:
            id = input("Enter transaction id : ")
            entry_delete_validation(id,db)
            input_incomplete = False
            return id

        except ValueError as reason:
            print(reason)
            
def ticker_delete(db):
    input_incomplete = True
    while input_incomplete == True:
        try:
            ticker = input("Enter ticker to delete : ")
            ticker_delete_validation(ticker,db)
            input_incomplete = False
            return ticker

        except ValueError as reason:
            print(reason)

# Input loops
def transaction_type_input():
    input_incomplete = True
    while input_incomplete == True:
        try:
            trans_type = input("Enter transaction type (Buy or Sell) : ")
            transaction_type_validation(trans_type)
            input_incomplete = False
            return trans_type

        except ValueError as reason:
            print(reason)

def stock_ticker_input():
    input_incomplete = True
    while input_incomplete == True:
        try:
            ticker = input("Enter stock ticker : ")
            stock_ticker_validation(ticker)
            input_incomplete = False
            return ticker

        except ValueError as reason:
            print(reason)

def transaction_date_input():
    input_incomplete = True
    while input_incomplete == True:
        try:
            date_entry = input('Enter a date in YYYY-MM-DD format : ')
            year, month, day = map(int, date_entry.split('-'))
            datetime.date(year, month, day)
            input_incomplete = False
            return date_entry

        except ValueError:
            print("Please enter a valid date.")

def stock_quantity_input():
    input_incomplete = True
    while input_incomplete == True:    
        try:
            quantity = input("Enter quantity bought : ")
            stock_quantity_validation(quantity)
            input_incomplete = False
            return quantity

        except ValueError as reason:
            print(reason) 

def stock_currency_input():
    input_incomplete = True
    while input_incomplete == True:
        try:
            currency = input("Enter stock currency (CAD or USD) : ")
            stock_currency_validation(currency)
            input_incomplete = False
            return currency

        except ValueError as reason:
            print(reason)

def stock_price_input():
    input_incomplete = True
    while input_incomplete == True:    
        try:
            price = input("Enter stock book value (price you paid per unit) : ")
            stock_price_validation(price)
            input_incomplete = False
            return price

        except ValueError as reason:
            print(reason)

def brokerage_fee_input():
    input_incomplete = True
    while input_incomplete == True:    
        try:
            brokerage_fee = input("Enter the brokerage fee (broker commission - if none, enter 0) : ")
            brokerage_fee_validation(brokerage_fee)
            input_incomplete = False
            return brokerage_fee

        except ValueError as reason:
            print(reason)


#Validation
def transaction_type_validation(trans_type):
    if trans_type.upper() == "BUY":
        return "Buy"

    elif trans_type.upper() == "SELL":
        return "Sell"

    else:
        raise ValueError("Error - Please select a valid transaction type (Buy or Sell)")

def stock_ticker_validation(ticker):
    if not (3 <= len(ticker) <= 4):
        print(str("Ticker you entered "+"("+ ticker +") does not respect the convetional naming convention. \n Are you sure you correctly entered the ticker ? If ticker is incorrect, stock data wont be retrieved."))
        correct_ticker = input("Continue with current ticker (y/n)")
        if correct_ticker == "n":
            raise ValueError("Error - Please enter a new ticker.")

def stock_currency_validation(currency):
    if currency.upper() == "CAD":
        return "CAD"

    elif currency.upper() == "USD":
        return "USD"

    else:
        raise ValueError("Error - Please select a valid currency (CAD or USD). Other currencies are not supported yet.")

def stock_quantity_validation(quantity):
    try :
        if int(quantity) <= 0:
            raise ValueError("Error - Please select a valid quantity (must be greater than 0).")

    except ValueError:
        raise ValueError("Error - Please enter a valid quantity (must be greater than 0 and not be a string).")

def stock_price_validation(price):
    if float(price) <= 0:
        raise ValueError("Error - Please select a valid price (must be greater than 0).")

def brokerage_fee_validation(brokerage_fee):
    if float(brokerage_fee) < 0:
        raise ValueError("Error - Please select a valid fee (must be greater or equal to 0).")
    
def entry_delete_validation(id,db):
    if len(db.get_portfolio_transaction_id(id)) == 0:
        raise ValueError("Error - Please select a valid transaction ID.")
    
def ticker_delete_validation(ticker,db):
    if len(db.get_watchlist_ticker_entry(ticker)) == 0:
        raise ValueError("Error - Please select a valid ticker.")

#TO DO
def choose_portfolio_currency_display(database):
    pass