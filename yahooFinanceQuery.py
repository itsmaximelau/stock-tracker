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
        current_price = cleanDataYahooFloat(soup.find("span",{"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}))
        previous_close_price = cleanDataYahooFloat(data[0])
        day_variance = round((current_price - previous_close_price),2)
        day_variance_percent = round((((current_price - previous_close_price)/previous_close_price)*100),2)
        open_price = cleanDataYahooFloat(data[1])
        bid = cleanDataYahooStr(data[2])
        ask = cleanDataYahooStr(data[3])
        day_range = cleanDataYahooStr(data[4])
        week_52_range = cleanDataYahooStr(data[5])
        volume = cleanDataYahooInt(data[6])
        avg_volume = cleanDataYahooInt(data[7])
        market_cap = cleanDataYahooStr(data[8])
        beta = cleanDataYahooFloat(data[9])
        pe_ratio = cleanDataYahooFloat(data[10])
        eps = cleanDataYahooFloat(data[11])
        earnings_date = cleanDataYahooStr(data[12])
        forward_dividend = cleanDataYahooStr(data[13])
        ex_div_date = cleanDataYahooStr(data[14])
        target_1y = cleanDataYahooFloat(data[15])

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
        "target_1y" : target_1y
    }
    return data

def cleanDataYahooInt(tag):
    if tag.text == "N/A":
        return tag.text
    
    else:
        return int(((tag.text).replace(',', '')))

def cleanDataYahooFloat(tag):
    if tag.text == "N/A":
        return tag.text

    else:
        return round(float(((tag.text).replace(',', ''))),2)

def cleanDataYahooStr(tag):
    return tag.text
