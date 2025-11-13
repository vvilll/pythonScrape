#!/usr/bin/env python3 
import os
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scraper():
    URL = "https://finance.yahoo.com/markets/world-indices/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    page = requests.get(URL, headers=headers)
    # #print(results.prettify())
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="svelte")
    #store symbol, name, and price
    stockSymbols = results.find_all("span", class_="symbol yf-90gdtp")
    stockNames = results.find_all("div", class_="leftAlignHeader companyName yf-362rys enableMaxWidth")
    stockPrices = results.find_all("fin-streamer")
    #check for .finance file create if it does not exist
    if os.path.exists('.finance'):
        pass
    else:
        os.makedirs('.finance')

    for arg in (sys.argv[1:]): #go through each of the stock user includes in cmd line
        arg = arg.upper()
        for index in range(len(stockSymbols)):
            if arg == (stockSymbols[index].text.strip())[1:]: #check if user symbol equals one in the world stokc indexes
                usrPrice = stockPrices[index*6].text.strip()
                print(stockNames[index].text.strip() + '\n' + 'Current price is $' + stockPrices[index*6].text.strip())
                filefound = 0
                for file in os.listdir('.finance'):
                    if file.startswith(arg): #check if file for stock has been created
                        fileFound = 1
                        oldFile = '.finance/' + file
                        stock = open(oldFile, 'r')
                        oldStockPrice = stock.readline().strip()
                        print('The old price was $' + oldStockPrice)
                        priceDiff = float(oldStockPrice.replace(',','')) - float(usrPrice.replace(',',''))
                        if priceDiff < 0:
                            print('Price decreased by $' + "{:.2f}".format(priceDiff) + ' since you last check on ' + file[4:14] + ' ' + file[15:] + '\n') 
                        elif priceDiff > 0:
                            print('Price increased by $' + "{:.2f}".format(priceDiff) + ' since you last check on ' + file[4:14] + ' ' + file[15:] + '\n') 
                        else:
                            print('Price has not changed since you last check on ' + file[4:14] + ' ' + file[15:] + '\n')
                        os.remove('.finance/' + file)

                flName = '.finance/' + arg + '_' + datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                open(flName, 'x')
                fd = open(flName, 'w')
                fd.write(usrPrice + '\n')
                fd.close()

if __name__ == "__main__":
    scraper()