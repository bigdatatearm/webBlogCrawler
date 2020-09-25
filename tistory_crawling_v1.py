from brunch_get_url_v1 import get_url
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
    try:
        title = ''
        if soup.select("h3.tit_post"):
            tmp_list = []
            for i in soup.select("h3.tit_post"):
                tmp_list.append(i.text)
            tmp = ''.join(tmp_list)
            title = tmp

        elif soup.find(class_="title_view"):
            title = soup.find(class_="title_view").text
            
        elif soup.select("div.inner h1"):
            tmp_list = []
            for i in soup.select("div.inner h1"):
                tmp_list.append(i.text)
            if len(tmp_list) == 1:
                title = tmp_list[0]
            else:
                title = tmp_list[1]

        elif soup.select("div.hgroup h1"):
            tmp = ''
            for i in soup.select("div.hgroup h1"):
                tmp = i.text
            title = tmp

        elif soup.find(class_="txt_sub_tit"):
            title = soup.find(class_="txt_sub_tit").text
            
        elif soup.select("div.titleWrap h2 a"):
            tmp = ''
            for i in soup.select("div.titleWrap h2 a"):
                tmp = tmp + i.text
            title = tmp

        elif soup.select("div h2 a"):
            tmp_list = []
            for i in soup.select("div h2 a"):
                tmp_list.append(i.text)
            title = tmp_list[0]

        elif soup.find(class_='title-article'):
            title = soup.find(class_='title-article').text


        elif soup.find(class_='gh-headline'):
            title = soup.find(class_='gh-headline').text
            
            
        elif soup.select("h1 a"):
            for i in soup.select("h1 a"):
                title = i.text 

        title = re.sub('[~""\-=.#/?:$}<>|*]', '', title)
        title = title.replace("\n",'')
        title = title.strip()
        
    except:
        pass
    
    return title

def get_content(soup):
    point = 0
    try:
        contents = ''
        tmp_list = []

        if soup.select("div.entry-content p"):
            point = 3
            for i in soup.select("div.entry-content p"):
                i = i.text.strip()
                if len(i) >= 2:
                    tmp_list.append(i)
            contents = ''.join(tmp_list)

        elif soup.select(".tt_article_useless_p_margin p"):
            for i in soup.select(".tt_article_useless_p_margin p"):
                i = i.text.strip()
                tmp_list.append(i)
            contents = ''.join(tmp_list)
            
        elif soup.select("div.article p"):
            point = 4
            for i in soup.select("div.article p"):
                i = i.text.strip()
                if len(i) >= 2:
                    tmp_list.append(i)
            contents = ''.join(tmp_list)

        elif soup.find(class_="page-limit-width expand-support edge-support procode hljs-line hljs-stripe hljs-overflow fc useless-margin"):
            point = 5
            contents = soup.find(class_="page-limit-width expand-support edge-support procode hljs-line hljs-stripe hljs-overflow fc useless-margin").text

        elif soup.select(".e-content.post-content p"):
            point = 6
            for i in soup.select(".e-content.post-content p"):
                tmp = i.text.strip()
                if len(tmp) >= 2:
                    tmp_list.append(tmp)
            contents = ''.join(tmp_list)
            contents = contents.strip()
            
        elif soup.select("div#article p"):
            point = 7
            for i in soup.select("div#article p"):
                i = i.text.strip()
                if len(i) >= 2:
                    tmp_list.append(i)
            contents = ''.join(tmp_list)            
            
            
        elif soup.select("div.area_view p"):
            point = 1
            content = ''
            for i in soup.select('div.area_view p'):
                content = content+i.text
            contents = content
            
        
        contents = re.sub('[^0-9a-zA-Zㄱ-힗 .]', '', contents)
        
    except:
        pass
            
    return contents

def get_date(soup):
    date = ''
    try:
        if soup.select("span.meta span.date"):
            tmp_list = []
            for i in soup.select("span.meta span.date"):
                tmp_list.append(i.text)
            tmp = ''.join(tmp_list)
            datetime = ''
            for i in tmp.split('.'):
                i = i.strip()
                if len(i) == 1:
                    i = str(0) + i
                datetime = datetime+i
            date = datetime

        elif soup.select("span.info_post"):
            tmp_list = []
            for i in soup.select("span.info_post"):
                tmp_list.append(i.text)
            tmp = ''.join(tmp_list)
            tmp = tmp.split('\n')[1].strip()
            datetime = ''
            for i in tmp.split('.')[:-1]:
                i = i.strip()
                if len(i) == 1:
                    i = str(0) + i
                datetime = datetime+i
            date = datetime

        elif soup.select("div.date"):
            tmp_list = []
            for i in soup.select("div.date"):
                tmp_list.append(i.text.strip())
            tmp = ''.join(tmp_list)
            tmp_list = tmp.split('.')[:-1]
            datetime = ''
            for i in tmp_list:
                i = i.strip()
                if len(i) == 1:
                    i = str(0) + i
                datetime = datetime+i
            date = datetime

        elif soup.select("div.titleWrap span.date"):
            tmp_list = []
            for i in soup.select("div.titleWrap span.date"):
                tmp_list.append(i.text)
            tmp = ''.join(tmp_list)
            times = tmp.split('.')[:-1]
            datetime = ''
            for time in times:
                time = time.strip()
                if len(time) == 1:
                    time = str(0) + time
                datetime = datetime + time
            date = datetime

        elif soup.find(class_="jb-article-information-date"):
            days = soup.find(class_="jb-article-information-date").text.strip()
            datetime = ''
            for i in days.split('.'):
                i = i.strip()
                if len(i) == 1:
                    i = str(0)+i
                datetime = datetime+i
            date = datetime


        elif soup.find(class_='date'):
            days = soup.find(class_='date').text
            datetimes = ''
            for i in days.split("."):
                if ":" not in i:
                    i = i.strip()
                    if len(i) == 1:
                        i = str(0) + i
                    datetimes = datetimes + i
            date = datetimes

        elif soup.select('time'):
            for i in soup.select('time'):
                days = i.text
            tmp = days.split(" ")[0]
            datetimes = ''
            for i in tmp.split('.'):
                i = i.strip()
                if len(i) == 1:
                    i = str(0) + i
                datetimes = datetimes + i
            date = datetimes

    except:
        pass
        
    return date

def get_jpg(soup, title, i):
    try:
        if not(os.path.isdir('./tistory/'+title)):
            os.makedirs(os.path.join('./tistory/'+title))
    except OSError:
            print("Failed to create directory")
        
    cnt = 0
    try:
        http = "https:"
        if soup.select(".e-content.post-content img"):
            for img in soup.select(".e-content.post-content img"):
                src = img['src']
                if http not in src:
                    src = http+src
                urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
        
        elif soup.select(".jb-column.jb-column-content img"):
            for img in soup.select(".jb-column.jb-column-content img"):
                src = img['src']
                if http not in src:
                    src = http+src
                    urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
        
        elif soup.select("div.area_view img"):
            for img in soup.select('div.area_view img'):
                src = img['src']
                if http not in src:
                    src = http+src
                if 'ads' in src:
                    pass
                else:
                    urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1

        elif soup.select(".tt_article_useless_p_margin img"):
            for img in soup.select(".tt_article_useless_p_margin img"):
                src = img['src']
                if http not in src:
                    src = http+src
                urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
                
        elif soup.select(".article img"):
            for img in soup.select(".article img"):
                src = img['src']
                if http not in src:
                    src = http+src
                urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg') 
                cnt+=1
                
        elif soup.select(".article_view jpg")        :
            for img in soup.select(".article_view img"):
                src = img['src']
                if http not in src:
                    src = http+src
                urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
        
        elif soup.select(".entry-content img"):
            for img in soup.select(".entry-content img"):
                src = img['src']
                if http not in src:
                    src = http+src
                urllib.request.urlretrieve(src, './tistory/'+title+'/'+str(i)+'_'+str(cnt)+'.jpg')
                cnt+=1
                
    except:
        pass
    
    return cnt

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

data = pd.read_excel("tistory_url.xlsx")
url_list = list(data['url'])
my_result = crawler(url_list)
pd.DataFrame.from_dict(my_result, orient='index')