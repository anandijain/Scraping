import os.path
import bs4

import requests as r
from bs4 import BeautifulSoup

save_path = '.'


def open_page(url):
    site = r.get(url)
    page_html = site.content
    page = BeautifulSoup(page_html, "html.parser")
    return page


def open_file(file_name):
    name_of_file = file_name
    # add specifications for csv or text file via arg check if !(csv | txt) return nona
    complete_name = os.path.join(save_path, name_of_file + ".csv")
    # line below probably better called in caller or add another arg
    file1 = open(complete_name, "a", encoding="utf-8")
    return file1
