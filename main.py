from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import os
import portfolio
import stocktracker

# Create DB
if not os.path.isfile("portfolio.sqlite"):
        portfolio.createDatebase()

if __name__ == "__main__":
    ### CLI MENU ###
    menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_OUTER_LIGHT_INNER_BORDER) \
        .set_title_align('center') \
        .set_subtitle_align('center') \
        .set_left_margin(4) \
        .set_right_margin(4) \
        .show_header_bottom_border(True)    
    
    menu = ConsoleMenu("Stock Tracker", formatter=menu_format)
    
    # Portfolio
    # Menu
    portfolio_manager = ConsoleMenu(title="Manage Portfolio", formatter=menu_format)
    portfolio_manager_option = SubmenuItem("Manage Portfolio",submenu=portfolio_manager)
    portfolio_manager_option.set_menu(menu)
    menu.append_item(portfolio_manager_option)
    # Options
    addTransaction = items.FunctionItem("Add a transaction", portfolio.addTransaction)
    deleteTransaction = items.FunctionItem("Delete a transaction", portfolio.deleteTransaction)
    viewTransactions = items.FunctionItem("View transactions", portfolio.viewTransactions)
    choosePortfolioCurrencyDisplay = items.FunctionItem("Choose portfolio currency displayed", portfolio.choosePortfolioCurrencyDisplay)
    portfolio_manager.append_item(addTransaction)
    portfolio_manager.append_item(deleteTransaction)
    portfolio_manager.append_item(viewTransactions)
    portfolio_manager.append_item(choosePortfolioCurrencyDisplay)    
    
    # Watchlist
    # Menu
    watchlist = ConsoleMenu(title="Manage Watchlist", formatter=menu_format)
    watchlist_option = SubmenuItem("Manage Watchlist",submenu=watchlist)
    watchlist_option.set_menu(menu)
    menu.append_item(watchlist_option)
    
    # Options
    addToWatchList = items.FunctionItem("Add to watchlist", portfolio.addToWatchList)
    watchlist.append_item(addToWatchList)

    # Stock tracker
    launchStockTracker = items.FunctionItem("Launch stock tracker", stocktracker.launchTracker)
    menu.append_item(launchStockTracker)

    menu.show()