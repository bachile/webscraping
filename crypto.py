
from urllib.request import urlopen
from bs4 import BeautifulSoup


webpage = 'https://coinmarketcap.com/'

page = urlopen(webpage)			

soup = BeautifulSoup(page, 'html.parser')

title = soup.title

print("\n" + title.text)

table_rows = soup.findAll('tr')

for entry in table_rows[1:6]:
    td = entry.findAll("td")
    name = entry.find("p", class_ = "sc-4984dd93-0 kKpPOn").text
    symbol = entry.find("p", class_ = "sc-4984dd93-0 iqdbQL coin-item-symbol").text
    price = td[3].text
    change = td[5].text
    caret = entry.find('span', class_ = "sc-6a54057-0 iEhQde")

    if "icon-Caret-down" in caret.span['class']:
        p_m = '-'
    elif "icon-Caret-up" in caret.span['class']:
        p_m = '+'
    else:
        p_m = ''

    print()
    print(f'Name: {name}')
    print(f'Symbol: {symbol}')
    print(f'Current Price: {price}')
    print(f'Percent change in last 24 hours: {p_m}{change}')
    change = change.strip('%')
    price = price.replace('$','').replace(',','')
    if p_m == '-':
        og_price = float(price)/(1-(float(change)/100))
    elif p_m == '+':
        og_price = float(price)/(1+(float(change)/100))
    else:
        og_price = float(price)
    print(f'Before Change: ${og_price:,.2f}')

print()

