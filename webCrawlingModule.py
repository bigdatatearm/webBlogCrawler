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

    def selenium_crawling(self, blog_url):
        web_driver = webdriver.Chrome('./driver/ver85/chromedriver')
        web_driver.implicitly_wait(3)
        # iframe내의 html 추출
        web_driver.get(blog_url)
        iframes = web_driver.find_elements_by_tag_name("iframe")

        web_driver.switch_to.frame(iframes[0])

        # craling 데이터와 이미지데이터 반환
        crawlingData, blogImageList = self.beautifulsoupcrawling(web_driver.page_source, blog_url)


        if crawlingData == None:
            print("오류블로그 : ", blog_url)
            return None
        else:
            return crawlingData
            # imageSave(blogImageList, crawlingData[0])


    def beautifulsoupcrawling(self, page_source, blog_url):
        bsObject = bs(page_source, "html.parser")

        today = datetime.datetime.today()
        # print(bsObject)
        try:
            #정규식으로 공백제거
            pattern = re.compile(r'\n|\r')
            if bsObject.find("div", {"class": "pcol1"}) == None:
                #타이틀 크로링
                title = bsObject.find("span", {"class": "pcol1 itemSubjectBoldfont"}).text
                reTitle = re.sub(pattern, '', title)
                # 날짜 크로링
                blogDate = bsObject.find("p", {"class": "date fil5 pcol2 _postAddDate"}).text
                # if not len(blogDate.split('시간')) == 1:
                #     blogDate = today - datetime.timedelta(hours=int(blogDate.split('시간')[0]))
                # 블로그 본 크로링
                blogMainContant = bsObject.find("div", {"id": "postViewArea"})
            else:
                #타이틀 크로링
                title = bsObject.find("div", {"class": "pcol1"}).text
                reTitle = re.sub(pattern, '', title)
                # 날짜 크로링
                blogDate = bsObject.find("span", {"class": "se_publishDate pcol2"}).text

                # if not len(blogDate.split('시간')) == 1:
                #     blogDate = today - datetime.timedelta(hours=int(blogDate.split('시간')[0]))
                # 블로그 본 크로링
                blogMainContant = bsObject.find("div", {"class": "se-main-container"})
            # 이미지주소 크로링
            blogImages = blogMainContant.find_all("img")
            blogImageList = []

            for blogImage in blogImages:
                url = blogImage.attrs['src']
                blogImageList.append(url)

            reBlogMainContant = re.sub(pattern, '', blogMainContant.text)

            crawlingData = [reTitle, blog_url, blogDate, reBlogMainContant]

            # print(len(blogImageList))

            # print("crawling save")
        except AttributeError as err:
            print(err)
            return None, None

        except UnexpectedAlertPresentException as err:
            print(err)
            return None, None

        return crawlingData, blogImageList