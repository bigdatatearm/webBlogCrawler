import sys
import os
import pandas as pd
import numpy as np
import datetime
from datetime import datetime 
from dateutil.relativedelta import relativedelta


from bs4 import BeautifulSoup
from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import re
import csv

def get_naver_url(keyword, start, end):
    
    # keyword = "국내여행"
    # url을 저장할 url list
    url_list = []

    path = "chromedriver.exe"

    driver = webdriver.Chrome(path)

    driver.get('https://www.naver.com')

    time.sleep(2)

    # keyword 입력, 검색
    element = driver.find_element_by_id("query")
    element.send_keys(keyword)
    element.submit()

    # 블로그 선택
    driver.find_element_by_link_text("블로그").click()

    # 검색옵션 선택
    driver.find_element_by_link_text("검색옵션").click()

    # 기간 설정
    driver.find_element_by_xpath("""//*[@id="snb"]/div/ul/li[2]/a""").click()

    # 8년전 이면 10만건 나와서 8년으로 설정
    # year = str(datetime.today().year)
    # month = str(datetime.today().month)
    # day = str(datetime.today().day)
    # if len(day) ==  1:
    #     day = str(0) + day
    # start = str(int(year)-8)+month+day
    # end = year + month + day

    # 시작일
    start_date = driver.find_element_by_xpath("""//*[@id="blog_input_period_begin"]""")
    start_date.send_keys(start)
    
    time.sleep(1)
    
    # 종료일
    end_date = driver.find_element_by_xpath("""//*[@id="blog_input_period_end"]""")
    end_date.send_keys(end)

    time.sleep(0.5)
    
    # 기간 적용하기
    driver.find_element_by_class_name('tx').click()

    time.sleep(0.5)
    
    # 영역을 제목으로 지정
    driver.find_element_by_xpath("""//*[@id="snb"]/div/ul/li[3]/a""").click()
    driver.find_element_by_link_text("제목").click()

    time.sleep(0.5)
    
    # 검색 결과 블로그 수
    title_num = driver.find_element_by_class_name("title_num")
    title_num = title_num.text
    test = title_num.split("/")[-1]
    total = int("".join(re.findall("\d+",test)))

    if total > 10000:
        total_page = 1000

    else:
        total_page = int(total / 10) + 1

    for i in range(1, total_page):
        i = i*10 + 1
        url = "https://search.naver.com/search.naver?date_from={0}&date_option=8&date_to={1}\
&dup_remove=1&nso=a%3At%2Cp%3Afrom{2}to{3}\
&post_blogurl=&post_blogurl_without=&query={4}\
&sm=tab_pge&srchby=title&st=sim&where=post&start={5}".format(start, end, start, end, keyword, i)

        driver.get(url)

        # URL 크롤링 시작
        titles = "a.sh_blog_title._sp_each_url._sp_each_title"
        article_raw = driver.find_elements_by_css_selector(titles)

        time.sleep(0.5)
        
        for article in article_raw:
            url = article.get_attribute('href')
            url_list.append(url)
            
        if len(url_list) == 1000:
            driver.close()
            break
        
        if (i-1)/10 == total_page:
            driver.close()
            break
            
    return url_list, start

def get_times(date):
    date_list = []
    tmp = []
    start_date = datetime.strptime(date, '%Y%m%d')
    tmp.append(start_date)
    end_date = datetime.strptime(date, '%Y%m%d') - relativedelta(months=1)
    tmp.append(end_date)
    
    for date in tmp:
        year = str(date.year)
        month = str(date.month)
        if len(month) == 1:
            month = str(0) + month
        day = str(date.day)
        if len(day) == 1:
            day = str(0) + day
        tmp_date = year + month + day
        date_list.append(tmp_date)

    return date_list

def get_str_date(date):
    year = str(date.year)
    month = str(date.month)
    if len(month) == 1:
        month = str(0) + month
    day = str(date.day)
    if len(day) == 1:
        day = str(0) + day
    date = year + month + day
    return date
