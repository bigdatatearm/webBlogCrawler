import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def getURL(search, path):
    driver = webdriver.Chrome(path)
    driver.get("https://naver.com")
    driver.find_element_by_link_text("블로그").click()
    user_search = driver.find_element_by_xpath("""//*[@id="header"]/div[1]/div/div[2]/form/fieldset/div/input""")
    user_search.send_keys(search)
    user_search.send_keys(Keys.RETURN)
    # driver.find_element_by_xpath("""//*[@id="snb"]/div[1]/div/div[1]/a[2]""").click()
    time.sleep(1)
    driver.find_element_by_xpath("""//*[@id="content"]/section/div[1]/div[2]/div/div/a""").click()
    driver.find_element_by_xpath("""//*[@id="content"]/section/div[1]/div[2]/div/div/div/a[3]""").click()
    time.sleep(1)
    count = driver.find_element_by_xpath("""//*[@id="content"]/section/div[1]/div[2]/span/span/em""").text
    count = int(count.replace(",",'').replace("건",""))

    if count >= 10000:
        count = int(10000/7)+1
    else:
        count = int(count/7)+1

    href_list = []


    if count == 0:
        count = 1

    try:
        for page in range(count):
            tmpPage = driver.page_source
            soup = BeautifulSoup(tmpPage, "html.parser")
            for link in soup.findAll("a", {"class" : "desc_inner"}):
                if 'href' in link.attrs:
                    href_list.append(link.attrs['href'])
            current_page = int(driver.current_url.split("&")[0][-1])

            next_path_num = (current_page+1)%10

            if next_path_num != 1 and next_path_num != 0:
                next_xpath = """//*[@id="content"]/section/div[3]/span[""" + str(next_path_num) + "]/a"
                driver.find_element_by_xpath(next_xpath).click()
                time.sleep(1)
            elif next_path_num == 0:
                next_xpath = """//*[@id="content"]/section/div[3]/span[10]/a"""
                driver.find_element_by_xpath(next_xpath).click()
                time.sleep(1)        
            else:
                driver.find_element_by_link_text("다음").click()
                time.sleep(1)
    except:
        print("종료")
        return href_list

    return href_list