#!/usr/bin/env python3 
#   If needed run
#       sudo apt install python3-pip
#       pip3 install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

def scraper():
    URL = "https://finance.yahoo.com/markets/world-indices/"
    page = requests.get(URL)
    #print(results.prettify())
    soup = BeautifulSoup(page.content, "html.parser")



if __name__ == "__main__":
    scraper()