#!/usr/bin/env python3 
#   If needed run
#       sudo apt install python3-pip
#       pip3 install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def scraper():
    URL = "https://finance.yahoo.com/markets/world-indices/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    page = requests.get(URL, headers=headers)
    #print(results.prettify())
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="svelte")
    stockSymbols = results.find_all("span", class_="symbol yf-90gdtp")
    stockNames = results.find_all("div", class_="leftAlignHeader companyName yf-362rys enableMaxWidth")
    stockPrices = results.find_all("fin-streamer")
    for i in range(len(stockSymbols)):
        print(stockSymbols[i].text.strip() + "(" + stockNames[i].text.strip() + "): " +  stockPrices[i*6].text.strip())


if __name__ == "__main__":
    scraper()