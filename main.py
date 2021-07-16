from urllib.parse import quote_plus

import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
import excelcrawl
from openpyxl import load_workbook
def main():
    excelcrawl.excelcrawl.search_hotels_addr()


if __name__ == '__main__':
    main()