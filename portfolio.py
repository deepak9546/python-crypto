from requests import Request, Session
import json
from dateutil import parser
from simpledate import SimpleDate  #for converting timestamps 
from prettytable import PrettyTable
from colorama import Back, Fore, Style, init

init(convert=True)  #sometimes colorama doesn't work in cmd.exe
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
header = {
    'Accepts' : 'application/json',
    'X-CMC_PRO_API_KEY': 'b54bcf4d-1bca-4e8e-9a24-22ff2c3d462c' #put your api key here. it's a random key so no output ;)
}
session=Session()
session.headers.update(header)

convert='USD'
choice = input('Enter base currency for Portfolio (n for default):')
if choice != 'n':
    convert = choice.upper()

print()
print('####### My Portfolio #######')
print()
portfolio = 0.00
table = PrettyTable(['Asset', 'Amount Owned', convert + ' Value', 'Price', '1h', '24h', '7d'])
assets={}
with open('assets.txt') as inp:
    for line in inp:
        sym, amt = line.split()
        sym = sym.upper()
        assets[sym]=amt
        sym_str=','.join(assets)     #symbol string to pass in api call

parameters = { 'symbol' : sym_str, 
                'convert': convert}

response = session.get(url, params=parameters)
result = json.loads(response.text)
currency=result['data']
last_updated=0
for each in currency:
    name=currency[each]['name']
    symbol=currency[each]['symbol']
    quote = currency[each]['quote'][convert]
    hour_change = quote['percent_change_1h']
    day_change = quote['percent_change_24h']
    week_change = quote['percent_change_7d']
    price = quote['price']
    last_updated = quote['last_updated']
    value = float(price) * float(assets[symbol])
    if hour_change > 0:
        hour_change = Back.GREEN + Style.BRIGHT + str(hour_change) + ' %' + Style.RESET_ALL
    else:
        hour_change = Back.RED + str(hour_change) + ' %' + Style.RESET_ALL
    
    if day_change > 0:
        day_change = Back.GREEN + Style.BRIGHT + str(day_change) + ' %' + Style.RESET_ALL
    else:
        day_change = Back.RED + str(day_change) + ' %' + Style.RESET_ALL

    if week_change > 0:
        week_change = Back.GREEN + Style.BRIGHT + str(week_change) + ' %' + Style.RESET_ALL
    else:
        week_change = Back.RED + str(week_change) + ' %' + Style.RESET_ALL

    portfolio += value
    value_string = '{:,}'.format(round(value,2))

    table.add_row([name + ' (' + symbol + ')',
                   str(assets[symbol]),
                   value_string,
                   str(price),
                   str(hour_change),
                   str(day_change),
                   str(week_change)])

print(table)
print()
portfolio_value_string = '{:,}'.format(round(portfolio,2))
print('Total Portfolio Value: ' + Style.BRIGHT + Back.GREEN + portfolio_value_string + Style.RESET_ALL)
print()
time=parser.isoparse(last_updated)
last_updated_string = SimpleDate(time).convert(country='IN').naive.datetime
print('API Results Last Updated on ' + str(last_updated_string))
print()