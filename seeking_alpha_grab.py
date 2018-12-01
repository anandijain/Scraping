import os.path
import bs4
from bs4 import BeautifulSoup
from open_functions import open_page
from open_functions import open_file
from open_functions import proxy_open
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys
import unittest
import time
import re
from fake_useragent import UserAgent
import random
root_url = "https://seekingalpha.com"
profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3")
profile.set_preference("general.useragent.override", "Mozilla/5.0")
# global_driver = webdriver.Firefox(profile)


class CompanyGrab:
    def __init__(self, url_ext, file_name):
        self.driver = webdriver.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = root_url
        self.url_ext = url_ext
        # self.data = None;
        self.file_name = file_name
        self.verificationErrors = []
        self.accept_next_alert = True

    def grab_execute(self):
        file = open_file(self.file_name, "csv")
        driver = self.driver
        delay = 1.5
        driver.get(self.base_url + self.url_ext)
        # driver.find_element_by_link_text("All").click()
        for i in range(1, 3): # usually 350
            print(str(i) + "\n")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        parse_file_for_links(data, file, self.file_name) #arg 1 was data
        # print(str(data))
        # file.write(str(data))
        file.close()
        return data


# article name convention eg MSFT + (article num) 0 + date of article
def get_article_text(url, article_file_name):
    # while (True):
    print(str(url))
    page = proxy_open(url)

    article_file = open_file(article_file_name, "txt")
    main_content = page.find("div", {"id": "main_content"})
    if main_content is not None:
        article = main_content.div.article
        header = article.header
        if header is not None:
            print(str(header) + "\n")
        text = article.div
        if text is not None:
            print(str(text) + "\n")
        summary_wrap = article.find("div", {"class": "article-summary article-width"})
        if summary_wrap is not None:
            summary = summary_wrap.text
            print(str(summary) + "\n")
            article_file.write(str(summary) + "\n")
        all_text = article.find("div", {"class": "sa-art article-width"})
        if all_text is not None:
            article_file.write(str(all_text.text))
    if main_content is None:
        # if beautiful soup doesnt work, handly with selenium
        print("Most likely getting captcha error from seeking alpha, article text not received \n")
        article_file.write("Most likely getting captcha error from seeking alpha, article text not received \n")
    article_file.close()


def parse_file_for_links(data, file, company):
        page = BeautifulSoup(data, "html.parser")
        # article_container = page.find("div", {"class": "feed analysis"})
        # print(page.text)
        container = page.find("div", {"class": "content_block_investment_views"}).ul
        articles = container.find_all("li")
        article_number = 0
        for li in articles:
            # write each article title (maybe replace commas, maybe write this as a text file since its not a table
            datas = li.find_all("div")
            article = datas[1].find_all("div")
            info = article[0].a

            title = info.text
            # remove commas from title
            article_url = root_url + info['href']
            print(article_url)
            context = article[1].text.strip().split("•")
            author = context[0]
            author_url = article[1].a['href']
            date = context[1]
            comments = context[2]
            comment_count = comments.split("\xa0")[0]
            article_file_name = company + "_" + str(article_number) + "_" + date
            get_article_text(article_url, article_file_name)
            file.write(str(article_number) + "\n")
            time.sleep(1.5)
            # file.write(summary + '\n')
            print("Article Number: " + str(article_number) + "\n")
            # print(str(title) + '\n')
            # print(str(article_url) + '\n')
            # print(str(date) + '\n')
            # print(str(comment_count) + '\n')

            article_number += 1

# """
# AAPL = CompanyGrab("/symbol/AAPL?s=aapl", "AAPL")
# AAPL.grab_execute()

AMZN = CompanyGrab("/symbol/AMZN?s=amzn", "AMZN")
AMZN.grab_execute()

# MSFT = CompanyGrab("/symbol/MSFT?s=msft", "MSFT")
# MSFT.grab_execute()
# """

# get_article_text("https://seekingalpha.com/article/4223525-apple-vs-bank-america-tariffs-vs-rising-interest-rates", "test_AAPL2")
"""
rownum | date of article | title | path of article text"""

# proxy_grab()
