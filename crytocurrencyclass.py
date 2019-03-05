from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt


litecoin_link = 'https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20190101&end=20190305'
ethereum_link = 'https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20190101&end=20190305'
bitcoin_link = 'https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190101&end=20190305'


def bitcoin(link):
    bitcoin_r = requests.get(bitcoin_link)
    bitcoin_soup = BeautifulSoup(bitcoin_r.text, 'html.parser')
    bitcoin_table = bitcoin_soup.find('div', attrs={'class':'table-responsive'})
    rows = bitcoin_table.find_all('tr')
    data(rows)

def ethereum(link):
    ethereum_r = requests.get(ethereum_link)
    ethereum_soup = BeautifulSoup(ethereum_r.text, 'html.parser')
    ethereum_table = ethereum_soup.find('div', attrs={'class':'table-responsive'})
    rows = ethereum_table.find_all('tr')
    data(rows)

def litecoin(link):
    litecoin_r = requests.get(litecoin_link)
    litecoin_soup = BeautifulSoup(litecoin_r.text, 'html.parser')
    litecoin_table = litecoin_soup.find('div', attrs={'class':'table-responsive'})
    rows = litecoin_table.find_all('tr')
    data(rows)

def data(rows):
    data = []
    i = 0 # begin count
    for row in rows: # iterate through each row with tag 'tr' (table read)

        data_org = [] # make a list of lists
        find_children = row.findChildren() # find child nodes of parent node 'div' class='table'

        for children in find_children:
            data_org.append(children.text) # append all the 'child nodes'. data for each day.

        if(i > 0):
            data_org[0] = data_org[0].replace(',','') # remove comma in date string
            data_org[5] = data_org[5].replace(',','') # remove comma in total volume
            data_org[6] = data_org[6].replace(',','') # remove comma in market cap
            data.append({'date':dt.strptime(data_org[0], '%b %d %Y'), # format the date
                        'open':float(data_org[1]), # turn string in list into floats, append to main list
                        'high':float(data_org[2]), # make data into a dictionary
                        'low':float(data_org[3]),
                        'close':float(data_org[4]),
                        'volume':float(data_org[5]),
                        'mcap':float(data_org[6])})

        i = i + 1 # counter

    data_frame = pd.DataFrame(data)
    print(data_frame)

def main():
    bitcoin(bitcoin_link)
    ethereum(ethereum_link)
    litecoin(litecoin_link)
    


if __name__ == '__main__': main()