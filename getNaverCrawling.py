from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

from getNaverURL import getURL
from get_naver import get_naver


def getNaverBlog(url_list, path):
    df = pd.DataFrame(columns=['title','writedate','blogurl','maincontant'])
    for url in url_list:
        driver = webdriver.Chrome(path)
        driver.get(url)
        iframes = driver.find_elements_by_tag_name('iframe')
        driver.switch_to.frame(iframes[0])

        source_code = driver.page_source
        driver.close()

        soup = BeautifulSoup(source_code, "html.parser")

        gn = get_naver()
        
        crawlingData = gn.get_data(soup, url)
        df = df.append({"title" : crawlingData[0], "writedate" : crawlingData[1], 
                        'blogurl' : url, 'maincontant' : crawlingData[-1]}, ignore_index=True)

        df.to_csv("tmp.csv", encoding='utf-8', index=False)
    return 

if __name__ == "__main__":
    path = "chromedriver.exe"
    url_list = getURL("한화 해체", path)
    getNaverBlog(url_list, path)
