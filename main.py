from consolemenu import *
from consolemenu.format import *
from consolemenu.items import *
from pathlib import Path
import stocktracker
import cli


# Variables
REFRESH_RATE = 45
DB_NAME = "StockData"

# Objects
my_database = stocktracker.Database(DB_NAME)
my_portfolio = stocktracker.Portfolio(my_database)
my_watchlist = stocktracker.Watchlist(my_database)
tracker = stocktracker.Tracker(REFRESH_RATE,my_database)

### CLI MENU ###
menu_format = MenuFormatBuilder().set_border_style_type(MenuBorderStyleType.DOUBLE_LINE_OUTER_LIGHT_INNER_BORDER) \
    .set_title_align('center') \
    .set_subtitle_align('center') \
    .set_left_margin(4) \
    .set_right_margin(4) \
    .show_header_bottom_border(True)
    
menu = ConsoleMenu("Stock Tracker", formatter=menu_format)

## Portfolio

# Menu
portfolio_manager = ConsoleMenu(title="Manage Portfolio", formatter=menu_format)
portfolio_manager_option = SubmenuItem("Manage Portfolio",submenu=portfolio_manager)
portfolio_manager_option.set_menu(menu)
menu.append_item(portfolio_manager_option)

# Options
add_transaction = items.FunctionItem("Add a transaction", cli.add_transaction,(my_database,my_portfolio))
delete_transaction = items.FunctionItem("Delete a transaction", cli.delete_transaction,(my_database,my_portfolio))
view_transactions = items.FunctionItem("View transactions", cli.view_transactions,([my_database]))
choose_portfolio_currency_display = items.FunctionItem("Choose portfolio currency displayed", cli.choose_portfolio_currency_display)
portfolio_manager.append_item(add_transaction)
portfolio_manager.append_item(delete_transaction)
portfolio_manager.append_item(view_transactions)
portfolio_manager.append_item(choose_portfolio_currency_display)    

## Watchlist

# Menu
watchlist = ConsoleMenu(title="Manage Watchlist", formatter=menu_format)
watchlist_option = SubmenuItem("Manage Watchlist",submenu=watchlist)

watchlist_option.set_menu(menu)
menu.append_item(watchlist_option)

# Options
add_to_watchlist = items.FunctionItem("Add to watchlist", cli.add_to_watchlist,(my_database,my_watchlist))
delete_from_watchlist = items.FunctionItem("Delete from watchlist", cli.delete_from_watchlist,(my_database,my_watchlist))
view_watchlist = items.FunctionItem("View watchlist", cli.view_watchlist_tickers,([my_database]))
watchlist.append_item(add_to_watchlist)
watchlist.append_item(delete_from_watchlist)
watchlist.append_item(view_watchlist)

# Stock tracker
launch_stock_tracker = items.FunctionItem("Launch stock tracker", tracker.launch_tracker)
menu.append_item(launch_stock_tracker)

menu.show()
