#!/usr/bin/env python3 
#   If needed run
#       sudo apt install python3-pip
#       pip3 install requests beautifulsoup4
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
    stockSymbols = results.find_all("span", class_="symbol yf-90gdtp")
    stockNames = results.find_all("div", class_="leftAlignHeader companyName yf-362rys enableMaxWidth")
    stockPrices = results.find_all("fin-streamer")
    if os.path.exists('.finance'):
        pass
    else:
        os.makedirs('.finance')

    for arg in (sys.argv[1:]):
        arg = arg.upper()
        for i in range(len(stockSymbols)):
            if arg == (stockSymbols[i].text.strip())[1:]:
                usrPrice = stockPrices[i*6].text.strip()
                print(stockNames[i].text.strip() + '\n' + 'Current price is $' + stockPrices[i*6].text.strip())
                filefound = 0
                for file in os.listdir('.finance'):
                    if file.startswith(arg):
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

                    


    

        # print(stockNames[i].text.strip() + "(" + (stockSymbols[i].text.strip())[1:] + "): " +  stockPrices[i*6].text.strip())
#need to print stock name
#then print price from webData
#then check finance folder for the stock
    #if the stock is in the folder print old stock price
    #then print difference between old price and new
    #then delete old file
#create file with stock price name being: <stockSymbol>_<yyyy-mm-dd>_<hh:mm:ss>




if __name__ == "__main__":
    scraper()