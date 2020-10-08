import sys
import os
import pandas as pd
import numpy as np
import datetime
from datetime import datetime 
from dateutil.relativedelta import relativedelta
from get_naver_url import get_naver_url, get_str_date, get_times 
from get_daum_tistory_url import get_daum_tistory_url
from get_brunch_url import get_brunch_url


from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import re
import csv


keyword = input()
url_list = []
tmp_list = get_daum_tistory_url(keyword)
url_list = url_list + tmp_list

tmp_list = get_brunch_url(keyword)
url_list = url_list + tmp_list
date = datetime.today()
date = get_str_date(date)
while len(url_list) <= 100000:
    tmp_times = get_times(date)
    end = tmp_times[0]
    start = tmp_times[1]
    tmp_list, date = get_naver_url("국내여행",start, end)
    url_list = url_list + tmp_list
    set(url_list)

urls = pd.DataFrame(url_list)
urls.to_csv("url_list.csv",header=False, index=False)
