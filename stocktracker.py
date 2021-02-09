import bs4
import requests
import sqlite3
import os
import time
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen


def getStockData(ticker):
    try:
        page = urlopen(str("https://finance.yahoo.com/quote/"+ticker))
        soup = bs4.BeautifulSoup(page,"html.parser")
        current_price = round(float(getCurrentPrice(ticker,soup)),2)
        previous_close_price = round(float(getPreviousClosePrice(ticker,soup)),2)
        day_variance = round((current_price - previous_close_price),2)
        return ticker,current_price,previous_close_price,day_variance

    except:
        print("Could not find ticker "+str(ticker)+".")

def getCurrentPrice(ticker, soup):
    try:
        price = str(soup.find("span",{"class": "Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)"}).text).replace(',', '')
        return price

    except:
        print("Error - could not find this stock price.")

def getPreviousClosePrice(ticker, soup):
    try:
        price = str(soup.find("td",{"class": "Ta(end) Fw(600) Lh(14px)"}).text).replace(',', '')
        return price

    except:
        print("Error - could not find this stock price.")

def getCurrentTime():
    return datetime.now().strftime("%H:%M:%S")

def printStockData(tickerInfo):
    print("--------------------")
    print("Ticker : "+str(tickerInfo[0]))
    print("Price : "+str(tickerInfo[1]))
    print("Open price : "+str(tickerInfo[2]))
    print("Variance : "+str(tickerInfo[3]))
    print("--------------------\n")

searchedTickerList = ["AMZN","SPY","GME"]

def main():

    while(True):
        print("\n   Stock Tracker \n")
        for ticker in searchedTickerList:
            printStockData(getStockData(ticker))
        print("Current time : " + getCurrentTime())
        time.sleep(60)
        os.system('cls' if os.name == 'nt' else 'clear')

main()


