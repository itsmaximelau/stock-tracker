import bs4
from urllib.request import urlopen

class YahooInfo:
    def __init__(self,ticker) -> None:
        self.ticker = ticker
    
    def get_ticker_data(self):
        # Connect to Yahoo Finance and get HTML.
        try:
            page = urlopen(str("https://finance.yahoo.com/quote/"+self.ticker))
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
            current_price = self.clean_data_float(soup.find("span",{"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text)
            
            available_stock_data = {}
            
            for i in range(0,16):
                to_add = {(data[i].attrs["data-test"]):(data[i]).text}
                available_stock_data.update(to_add)
            
            previous_close_price = self.clean_data_float(available_stock_data.get("PREV_CLOSE-value",None))
            open_price = self.clean_data_float(available_stock_data.get("OPEN-value",None))
            bid = self.clean_data_str(available_stock_data.get("BID-value",None))
            ask = self.clean_data_str(available_stock_data.get("ASK-value",None))
            day_range = self.clean_data_str(available_stock_data.get("DAYS_RANGE-value",None))
            week_52_range = self.clean_data_str(available_stock_data.get("FIFTY_TWO_WK_RANGE-value",None))
            volume = self.clean_data_int(available_stock_data.get("TD_VOLUME-value",None))
            avg_volume = self.clean_data_int(available_stock_data.get("AVERAGE_VOLUME_3MONTH-value",None))
            net_assets = self.clean_data_str(available_stock_data.get("NET_ASSETS-value",None))
            NAV = self.clean_data_float(available_stock_data.get("NAV-value",None))
            PE_ratio = self.clean_data_str(available_stock_data.get("PE_RATIO-value",None))
            stock_yield = self.clean_data_str(available_stock_data.get("TD_YIELD-value",None))
            YTD_daily = self.clean_data_str(available_stock_data.get("YTD_DTR-value",None))
            beta = self.clean_data_float(available_stock_data.get("BETA_5Y-value",None))
            expense_ratio = self.clean_data_str(available_stock_data.get("EXPENSE_RATIO-value",None))
            inception_date = self.clean_data_str(available_stock_data.get("FUND_INCEPTION_DATE-value",None))
            market_cap = self.clean_data_str(available_stock_data.get("MARKET_CAP-value-value",None))
            beta = self.clean_data_float(available_stock_data.get("BETA_5Y-value-value",None))
            pe_ratio = self.clean_data_float(available_stock_data.get("PE_RATIO-value",None))
            eps = self.clean_data_float(available_stock_data.get("EPS_RATIO-value",None))
            earnings_date = self.clean_data_str(available_stock_data.get("EARNINGS_DATE-value",None))
            forward_dividend = self.clean_data_str(available_stock_data.get("DIVIDEND_AND_YIELD-value",None))
            ex_div_date = self.clean_data_str(available_stock_data.get("EX_DIVIDEND_DATE-value",None))
            target_1y = self.clean_data_float(available_stock_data.get("ONE_YEAR_TARGET_PRICE-value",None))
            day_variance = round((current_price - previous_close_price),2)
            day_variance_percent = round((((current_price - previous_close_price)/previous_close_price)*100),2)

        except:
            raise Exception("Could not fetch data from Yahoo! Finance.")
            
        data = {
            "ticker": self.ticker,
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

    @staticmethod
    def clean_data_int(content):
        if content == "N/A" or content is None:
            return content
        
        else:
            return int(((content).replace(',', '')))

    @staticmethod
    def clean_data_float(content):
        if content == "N/A" or content is None:
            return content

        else:
            return round(float(((content).replace(',', ''))),2)

    @staticmethod
    def clean_data_str(content):
        return content

class Stock:
    def __init__(self,ticker) -> None:
        self.ticker = ticker
        self.data = YahooInfo(ticker).get_ticker_data()
        self.company_name = self.data["company_name"]
        self.current_price = self.data["current_price"]
        self.previous_close_price = self.data["previous_close_price"]
        self.open_price = self.data["open_price"]
        self.bid = self.data["bid"]
        self.ask = self.data["ask"]
        self.day_range = self.data["day_range"]
        self.week_52_range = self.data["week_52_range"]
        self.volume = self.data["volume"]
        self.avg_volume = self.data["avg_volume"]
        self.net_assets = self.data["net_assets"]
        self.NAV = self.data["NAV"]
        self.PE_ratio = self.data["PE_ratio"]
        self.stock_yield = self.data["stock_yield"]
        self.YTD_daily = self.data["YTD_daily"]
        self.beta = self.data["beta"]
        self.expense_ratio = self.data["expense_ratio"]
        self.market_cap = self.data["market_cap"]
        self.beta = self.data["beta"]
        self.pe_ratio = self.data["pe_ratio"]
        self.eps = self.data["eps"]
        self.earnings_date = self.data["earnings_date"]
        self.forward_dividend = self.data["forward_dividend"]
        self.ex_div_date = self.data["ex_div_date"]
        self.target_1y = self.data["target_1y"]
        self.day_variance = self.data["day_variance"]
        self.day_variance_percent = self.data["day_variance_percent"]