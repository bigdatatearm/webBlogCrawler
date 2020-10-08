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

def get_daum_tistory_url(keyword):
    
    path = "chromedriver.exe"

    for crawl in range(2,4):
        time.sleep(2)

        driver = webdriver.Chrome(path)
        driver.get("https://www.daum.net")
        
        # 검색어 입력
        element = driver.find_element_by_id("q")
        element.send_keys(keyword)
        element.submit()

        time.sleep(1)
        
        # 블로그 카테고리 선택, 클릭
        driver.find_element_by_link_text("블로그").click()

        # 출처 전체 클릭
        driver.find_element_by_xpath("""//*[@id="blogColl"]/div[2]/div[1]/a""").click()

        # Daum블로그 선택
        tmp_path = """//*[@id="blogColl"]/div[2]/div[1]/div/ul/li[{0}]/a""".format(crawl)
        driver.find_element_by_xpath(tmp_path).click()


        # 기간 설정
        driver.find_element_by_xpath("""//*[@id="blogColl"]/div[2]/div[2]/a""").click()

        # 4 : 1개월 - daum_blog:728, 티스토리:3,440
        # 5 : 6개월 - daum_blog:6340, 티스토리:19,400
        # 6 : 1년 - daum_blog:10,400, 티스토리:32,600
        # 현재는 1년을 함
        xpath = """//*[@id="blogColl"]/div[2]/div[2]/div/ul/li[6]/a"""
        driver.find_element_by_xpath(xpath).click()


        # 날짜, 시간
        now = datetime.now()
        nowTime = str(now.strftime('%H%M%S'))
        day = str(now.strftime("%Y%m%d"))
        one_year = str(int(day) - 10000)

        # Page 수 확인
        total = driver.find_element_by_xpath("""//*[@id="blogColl"]/div[1]/div[2]/span""")
        tmp_page = total.text
        num = tmp_page.find("/")
        total_num = tmp_page[num+2:-1]

        if len(total_num) <= 4:
            if ',' in total_num:
                total_page = int(total_num.replace(',',''))
            else:
                total_page = int(total_num)
        else:
            space = total_num.find(' ')
            total_num = total_num[space+1:-1]
            total_page = int(total_num.replace(',',''))
        url_list = []
        title_list = []

        tmp_target = ''
        if crawl == 2:
            tmp_target = 'SA=daumsec&'
        else:
            tmp_target = 'SA=tistory&'

        for i in range(1, total_page):
            stop = False
            url = "https://search.daum.net/search?nil_suggest=btn\
            &w=blog&DA=PGD&q={0}&f=section&{1}period=y&sd={2}&ed={3}&page={4}".format(keyword,tmp_target,one_year+nowTime, day+nowTime, i)
            driver.get(url)
            time.sleep(0.5)

            # URL 크롤링 시작
            titles = "a.f_link_b"
            article_raw = driver.find_elements_by_css_selector(titles)

            # URL 크롤링
            for article in article_raw:
                url = article.get_attribute("href")
                title = article.text
                url_list.append(url)
                title_list.append(title)
                if url_list.count(url) >= 2:
                    stop = True
            if stop == True:
                break

        while True:
            if url_list.count(url_list[-1]) == 2:
                url_list.pop()
                title_list.pop()
            else:
                break
                
    return url_list