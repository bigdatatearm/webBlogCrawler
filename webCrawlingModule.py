from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib import parse
from bs4 import BeautifulSoup as bs
import csv, re, os, datetime
import pandas as pd

class Crawler:
    def __init__(self, blogURL, title, date, mainContent):
        self.blogURL = blogURL
        self.title = title
        self.date = date
        self.mainContent = mainContent

    def selenium_crawling(self):


    def beautifulsoup_crawling(self):


    def pageMoving(self):