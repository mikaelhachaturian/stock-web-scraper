import bs4
import requests
from bs4 import BeautifulSoup as bsoup
import argparse
import time


YAHOO_URL = "https://finance.yahoo.com/quote/{0}?p={0}"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_stock_info(url):
    r = requests.get(url)
    soup = bsoup(r.text, "lxml")
    current_price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[
        0].find('span').text
    open_price = soup.find_all('td', {'class': 'Ta(end) Fw(600) Lh(14px)', 'data-test': 'OPEN-value'})[
        0].find('span').text
    try:
        close_price = soup.find_all('td', {'class': 'Ta(end) Fw(600) Lh(14px)', 'data-test': 'PREV_CLOSE-value'})[
            0].find('span').text
    except:
        close_price = "N/A (Currently open on market)"

    stock_info = {
        "current_price": current_price,
        "open_price": open_price,
        "close_price": close_price
    }
    return stock_info


def read_symbols_file():
    with open('stock_symbols.txt', 'r') as stock_symbol_file:
        content = stock_symbol_file.readlines()
        symbols = [x.strip() for x in content]
    return symbols


def print_all_prices(symbols):
    for symbol in symbols:
        stock_info = get_stock_info(YAHOO_URL.format(symbol))
        print(
            "{2}current price{3} for {7}{2}{4}{3} is {1}${0}{3} | {2}opening price{3} = ${5} | {2}previous closing price{3} = ${6}. ".format(stock_info["current_price"], bcolors.OKGREEN, bcolors.OKBLUE, bcolors.ENDC,
                                                                                                                                             symbol, stock_info["open_price"], stock_info["close_price"], bcolors.BOLD))


def define_parser():
    parser = argparse.ArgumentParser(
        description='Stock market web scraping tool.')
    parser.add_argument('-t', '--time', dest='time',
                        help='time (in seconds) to check stocks in loop.')
    parser.add_argument('-l', '--list', action='store_true',
                        help='list all prices for stocks.')
    return parser


def list_prices(args):
    symbols = read_symbols_file()
    print(f"{bcolors.BOLD}---------------- Stock Market Web Scraper ----------------{bcolors.ENDC}")
    if args.time:
        print(f"{bcolors.WARNING}Waiting {args.time} seconds each cycle.{bcolors.ENDC}")
        while True:
            print(f"{bcolors.HEADER}-----{bcolors.ENDC}")
            print_all_prices(symbols)
            print(
                f"{bcolors.HEADER}-----{bcolors.ENDC}\n")
            time.sleep(int(args.time))
    else:
        print_all_prices(symbols)


def main():
    args = define_parser().parse_args()
    if args.list:
        list_prices(args)
    else:
        define_parser().print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}Interrupted. Exiting.{bcolors.ENDC}")
        quit()
