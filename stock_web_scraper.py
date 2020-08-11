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


def get_price(url):
    r = requests.get(url)
    soup = bsoup(r.text, "lxml")
    price = soup.find_all('div', {'class': 'My(6px) Pos(r) smartphone_Mt(6px)'})[
        0].find('span').text
    return price


def read_symbols_file():
    with open('stock_symbols.txt', 'r') as stock_symbol_file:
        content = stock_symbol_file.readlines()
        symbols = [x.strip() for x in content]
    return symbols


def print_all_prices(symbols):
    for symbol in symbols:
        print(
            f"current price for {bcolors.OKBLUE}{symbol}{bcolors.ENDC} stock is {bcolors.OKGREEN}${get_price(YAHOO_URL.format(symbol))}{bcolors.ENDC}")


def define_parser():
    parser = argparse.ArgumentParser(
        description='Stock market web scraping tool.')

    parser.add_argument('-t', '--time', dest='time', default=10,
                        help='time (in seconds) to check stocks (default 10 seconds).')
    return parser


def main():
    args = define_parser().parse_args()
    symbols = read_symbols_file()
    print(f"{bcolors.BOLD}---------------- Stock Market Web Scraper ----------------{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Waiting {args.time} seconds each cycle.{bcolors.ENDC}")
    while True:
        print(f"{bcolors.HEADER}-----{bcolors.ENDC}")
        print_all_prices(symbols)
        print(
            f"{bcolors.HEADER}-----{bcolors.ENDC}\n")
        time.sleep(int(args.time))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{bcolors.FAIL}Interrupted. Exiting.{bcolors.ENDC}")
        quit()
