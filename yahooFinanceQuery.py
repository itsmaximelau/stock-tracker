import bs4
import logging
from urllib.request import urlopen

# Logging configs
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.WARNING)

def getStockData(ticker):
    # Connect to Yahoo Finance and get HTML.
    try:
        page = urlopen(str("https://finance.yahoo.com/quote/"+ticker))
        soup = bs4.BeautifulSoup(page,"html.parser")

    except:
        raise Exception("Could not connect to Yahoo Finance.")
    
    # Get summary table
    try:
        data = soup.find_all("td",{"class": "Ta(end) Fw(600) Lh(14px)"})  
        
    except:
        raise Exception("Could not find table.")
    
    # Separate data from table (isolate).
    try:
        company_name = soup.find("h1",{"class": "D(ib) Fz(18px)"}).text
        current_price = cleanDataYahooFloat(soup.find("span",{"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text)
        
        available_stock_data = {}
        
        for i in range(0,16):
            to_add = {(data[i].attrs["data-test"]):(data[i]).text}
            available_stock_data.update(to_add)
        
        previous_close_price = cleanDataYahooFloat(available_stock_data.get("PREV_CLOSE-value",None))
        open_price = cleanDataYahooFloat(available_stock_data.get("OPEN-value",None))
        bid = cleanDataYahooStr(available_stock_data.get("BID-value",None))
        ask = cleanDataYahooStr(available_stock_data.get("ASK-value",None))
        day_range = cleanDataYahooStr(available_stock_data.get("DAYS_RANGE-value",None))
        week_52_range = cleanDataYahooStr(available_stock_data.get("FIFTY_TWO_WK_RANGE-value",None))
        volume = cleanDataYahooInt(available_stock_data.get("TD_VOLUME-value",None))
        avg_volume = cleanDataYahooInt(available_stock_data.get("AVERAGE_VOLUME_3MONTH-value",None))
        net_assets = cleanDataYahooStr(available_stock_data.get("NET_ASSETS-value",None))
        NAV = cleanDataYahooFloat(available_stock_data.get("NAV-value",None))
        PE_ratio = cleanDataYahooStr(available_stock_data.get("PE_RATIO-value",None))
        stock_yield = cleanDataYahooStr(available_stock_data.get("TD_YIELD-value",None))
        YTD_daily = cleanDataYahooStr(available_stock_data.get("YTD_DTR-value",None))
        beta = cleanDataYahooFloat(available_stock_data.get("BETA_5Y-value",None))
        expense_ratio = cleanDataYahooStr(available_stock_data.get("EXPENSE_RATIO-value",None))
        inception_date = cleanDataYahooStr(available_stock_data.get("FUND_INCEPTION_DATE-value",None))
        market_cap = cleanDataYahooStr(available_stock_data.get("MARKET_CAP-value-value",None))
        beta = cleanDataYahooFloat(available_stock_data.get("BETA_5Y-value-value",None))
        pe_ratio = cleanDataYahooFloat(available_stock_data.get("PE_RATIO-value",None))
        eps = cleanDataYahooFloat(available_stock_data.get("EPS_RATIO-value",None))
        earnings_date = cleanDataYahooStr(available_stock_data.get("EARNINGS_DATE-value",None))
        forward_dividend = cleanDataYahooStr(available_stock_data.get("DIVIDEND_AND_YIELD-value",None))
        ex_div_date = cleanDataYahooStr(available_stock_data.get("EX_DIVIDEND_DATE-value",None))
        target_1y = cleanDataYahooFloat(available_stock_data.get("ONE_YEAR_TARGET_PRICE-value",None))
        day_variance = round((current_price - previous_close_price),2)
        day_variance_percent = round((((current_price - previous_close_price)/previous_close_price)*100),2)

    except:
        raise Exception("Could not seperate data from table.")
        
    data = {
        "ticker": ticker,
        "company_name" : company_name,
        "current_price" : current_price,
        "previous_close_price" : previous_close_price,
        "day_variance" : day_variance,
        "day_variance_percent" : day_variance_percent,
        "open_price" : open_price,
        "bid" : bid,
        "ask" : ask,
        "day_range" : day_range,
        "week_52_range" : week_52_range,
        "volume" : volume,
        "avg_volume" : avg_volume,
        "market_cap" : market_cap,
        "beta" : beta,
        "pe_ratio" : pe_ratio,
        "eps" : eps,
        "earnings_date" : earnings_date,
        "forward_dividend" : forward_dividend,
        "ex_div_date" : ex_div_date,
        "target_1y" : target_1y,
        "net_assets" : net_assets,
        "NAV" : NAV,
        "PE_ratio" : PE_ratio,
        "stock_yield" : stock_yield,
        "YTD_daily" : YTD_daily,
        "expense_ratio" : expense_ratio,
        "inception_date" : inception_date
    }
    return data

def cleanDataYahooInt(content):
    if content == "N/A" or content is None:
        return content
    
    else:
        return int(((content).replace(',', '')))

def cleanDataYahooFloat(content):
    if content == "N/A" or content is None:
        return content

    else:
        return round(float(((content).replace(',', ''))),2)

def cleanDataYahooStr(content):
    return content
