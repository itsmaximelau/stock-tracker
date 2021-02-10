import consolemenu as cm
import os
import portfolio
import stocktracker

# Create DB
if not os.path.isfile("portfolio.sqlite"):
        portfolio.createDatebase()

if __name__ == "__main__":
    ### CLI MENU ###
    menu = cm.ConsoleMenu("Stock Tracker & Portfolio Manager")

    #Portfolio
    addTransaction = cm.items.FunctionItem("Add a transaction", portfolio.addTransaction)
    deleteTransaction = cm.items.FunctionItem("Delete a transaction", portfolio.deleteTransaction)
    viewTransactions = cm.items.FunctionItem("View transactions", portfolio.viewTransactions)
    choosePortfolioCurrencyDisplay = cm.items.FunctionItem("Choose portfolio currency displayed", portfolio.choosePortfolioCurrencyDisplay)

    #Stock tracker
    launchStockTracker = cm.items.FunctionItem("Launch live stock tracker", stocktracker.launchTracker)

    menu.append_item(addTransaction)
    menu.append_item(deleteTransaction)
    menu.append_item(viewTransactions)
    menu.append_item(choosePortfolioCurrencyDisplay)
    menu.append_item(launchStockTracker)

    menu.show()