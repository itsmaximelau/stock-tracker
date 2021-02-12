from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
import os
import stocktracker
import cli


db_name = "testttt"
my_database = stocktracker.Database(db_name)
my_portfolio = stocktracker.Portfolio(my_database)
my_watchlist = stocktracker.Watchlist(my_database)

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
add_transaction = items.FunctionItem("Add a transaction", cli.add_transaction,(my_database,my_portfolio))
deleteTransaction = items.FunctionItem("Delete a transaction", cli.delete_transaction)
view_transactions = items.FunctionItem("View transactions", cli.view_transactions,([my_database]))
choosePortfolioCurrencyDisplay = items.FunctionItem("Choose portfolio currency displayed", cli.choose_portfolio_currency_display)
portfolio_manager.append_item(add_transaction)
portfolio_manager.append_item(deleteTransaction)
portfolio_manager.append_item(view_transactions)
portfolio_manager.append_item(choosePortfolioCurrencyDisplay)    

# Watchlist
# Menu
watchlist = ConsoleMenu(title="Manage Watchlist", formatter=menu_format)
watchlist_option = SubmenuItem("Manage Watchlist",submenu=watchlist)
watchlist_option.set_menu(menu)
menu.append_item(watchlist_option)

# Options
addToWatchList = items.FunctionItem("Add to watchlist", cli.add_to_watchlist)
watchlist.append_item(addToWatchList)

# Stock tracker
launchStockTracker = items.FunctionItem("Launch stock tracker", stocktracker.launch_tracker)
menu.append_item(launchStockTracker)

menu.show()
