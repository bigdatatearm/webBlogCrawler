
# coding: utf-8

# In[4]:

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


# In[5]:


# daum blog에서 제목 추출
def get_title(soup):
    if soup.select('strong > a'):
        title = soup.select('strong > a')
        tmp = []
        for i in title:
            tmp.append(i.text)
        title = tmp[0]
        title = re.sub('[~""\-=.#/?:$}<>|*]', '', title)
        if title[-1] == ' ':
            title = title[:-1]
    else:
        title = soup.find("h2").text
        title = re.sub('[~""\-=.#/?:$}<>|*]', '', title)
        if title[-1] == ' ':
            title = title[:-1]
    return title


# In[6]:


# daum blog에서 날짜 추출
def get_date(soup):
    if soup.find(class_='date'):
        date = soup.find(class_='date').text
        date = soup.find(class_='date').text
        date = date.replace(' ','')
        date = date[:-1].split('.')
        tmp =''
        for i in date:
            if len(i) == 1:
                i = '0'+i
            tmp+=i
        if '-' in tmp:
            tmp = tmp.replace('-','')
        date = int(tmp)

    else:
        date = soup.find(class_='cB_Tdate').text
        date = date.replace(' ','')
        date = date[:-1].split('.')
        date = date[:-1]
        tmp =''
        for i in date:
            if len(i) == 1:
                i = '0'+i
            tmp+=i
        date = int(tmp)
    return date


# In[7]:


# daum blog에서 내용 추출
def get_content(soup):
    if soup.find(class_="cContentBody"):
        content = soup.find(class_="cContentBody")
        tmp = []
        for i in content.select("p"):
            if not i.select('iframe'):
                tmp.append(i.text)
        content = ''.join(tmp)
    elif soup.find(class_="tt_article_useless_p_margin"):
        content = soup.find(class_="tt_article_useless_p_margin").select('p')
        tmp = []
        for i in content:
            tmp.append(i.text)
        content = ''.join(tmp)
    elif soup.find(class_='article-view'):
        content = soup.find(class_='article-view').text
    if len(content) <= 0:
        tmp = []
        for i in soup.select("br"):
            tmp.append(i.text)
        content = set(tmp)
        content = ''.join(content)
    return content


# In[8]:


def get_jpg(soup, title, i):
    try:
        if not(os.path.isdir(title)):
            os.makedirs(os.path.join(title))
    except OSError:
            print("Failed to create directory")
    images = soup.select('span > img')
    cnt = 0
    
    for img in images:
        src = img['src']
        src = urllib.parse.quote(src.encode('utf8'), '/:')
        urllib.request.urlretrieve(src, './'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
        cnt+=1


# In[11]:


def crawler(url_list):
    dict = {}
    for i in range(len(url_list)):
        try:
            url = url_list[i]
            target_info = {}

            path="chromedriver.exe"
            driver = webdriver.Chrome(path)
            driver.get(url)
            time.sleep(3)
            source_code = driver.page_source
            driver.close()
            soup = BeautifulSoup(source_code, "html.parser")
            title = get_title(soup)
            content = get_content(soup)
            date = get_date(soup)
            jpg = get_jpg(soup, title, i)
            target_info['datetime'] = date
            target_info['title'] = title
            target_info['content'] = content
            dict[i] = target_info
            print(title[:10], date, content[:20], "사진수:",jpg, "/",i)
        except:
            print(url)
            pass
    return dict

# In[ ]:


data = pd.read_excel('daum_blog_url.xlsx')
url_list = list(data['url'])
my_result = crawler(url_list)
pd.DataFrame.from_dict(my_result, orient='index')
