from urllib.error import HTTPError
from urllib import parse

import requests
from bs4 import BeautifulSoup
import urllib.request as req
import urllib
import re
import os
import pandas as pd
import time

from selenium.webdriver.common.keys import Keys
from selenium import webdriver

def get_title(soup):
    title = soup.find(class_="cover_title").text
    return title

def get_content(soup):
    contents = soup.select("div > p")
    content_list = []
    for content in contents:
        content_list.append(content.text)
    content_list = content_list[2:]
    content = ''.join(content_list)
    return content

def get_date(soup):
    month_dict = {'Jan':1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
    
    tmp = soup.find(class_="f_l date").text
    day = tmp.replace(".", '')
    day = day.split(' ')
    month = month_dict[day[0]]
    year = day[-1]
    day = day[1]
    date = int(str(year)+str(month)+str(day))
    return date

def get_jpg(soup, title, i):
    jpgs = soup.select("div > img")
    try:
        if not(os.path.isdir('./brunch/'+title)):
            os.makedirs(os.path.join('./brunch/'+title))
    except OSError as e:
        if e.errno != Errno.EEXIST:
            print("Failed to create directory!")
            raise
    
    cnt = 0
    for jpg in jpgs:
        src = 'https:' + jpg['src']
        # src = urllib.parse.quote(src.encode('utf8'), '/:')
        urllib.request.urlretrieve(src, './brunch/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
        cnt+=1
    return cnt

def crawler(url_list):
    dict = {}
    for i in range(len(url_list)):
        url = url_list[i]
        target_info = {}
        try:
            path = "chromedriver.exe"
            driver = webdriver.Chrome(path)
            driver.get(url)
            time.sleep(3)
            source_code = driver.page_source
            driver.close()
            soup = BeautifulSoup(source_code, "html.parser")
            title = get_title(soup)
            date = get_date(soup)
            content = get_content(soup)
            jpg = get_jpg(soup, title, i)
            target_info['datetime'] = date
            target_info['title'] = title
            target_info['content'] = content
            dict[i] = target_info
            print(title[:10], date, content[:20], url, "사진 수:", jpg)
        except:
            print(url)
            pass
    return dict

data = pd.read_excel("brunch_blog_url.xlsx")
url_list = list(data['url'])
result_dict = crawler(url_list)
result_df = pd.DataFrame.from_dict(result_dict, orient="index")
result_df.to_excel('brunch_crawling.xlsx')