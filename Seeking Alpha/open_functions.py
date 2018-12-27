import os.path
from bs4 import BeautifulSoup
import requests
import time
from random import shuffle

save_path = r'C:\Users\Anand\Programming\seeking_alpha'
headers = {'User-Agent': 'Mozilla/5.0'}


def get_proxies(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "lxml")
    https_proxies = filter(lambda proxy: "yes" in proxy.text,
                           soup.select("table.table tr"))
    for item in https_proxies:
        yield "{}:{}".format(item.select_one("td").text,
                             item.select_one("td:nth-of-type(2)").text)


def get_random_proxies_iter():
    proxies = list(get_proxies('https://www.sslproxies.org/'))
    shuffle(proxies)
    time.sleep(1)
    return iter(proxies)  # iter so we can call next on it to get the next proxy


def get_proxy(session, proxies, validated=False):
    session.proxies = {'https': 'https://{}'.format(next(proxies))}
    if validated:
        while True:
            try:
                return session.get('https://httpbin.org/ip').json()
            except Exception:
                session.proxies = {'https': 'https://{}'.format(next(proxies))}


def get_response(url):
    session = requests.Session()
    ua = UserAgent()
    print(ua)
    proxies = get_random_proxies_iter()
    while True:
        try:
            session.headers = {'User-Agent': 'Mozilla/5.0'}
            print(get_proxy(session, proxies, validated=True))  # collect a working proxy to be used to fetch a valid response
            return session.get(url)  # as soon as it fetches a valid response, it will break out of the while loop
        except StopIteration:
            raise  # No more proxies left to try
        except Exception:
            pass  # Other errors: try again


def proxy_open(url):
    response = get_response(url)
    page = BeautifulSoup(response.text, "html.parser")
    return page


def open_page(url):
    req = requests.get(url, headers=headers)
    page_html = req.text
    page = BeautifulSoup(page_html, "html.parser")
    return page


# csv or txt
def open_file(file_name, file_type):
    name_of_file = file_name
    complete_name = os.path.join(save_path, name_of_file + "." + file_type) # txt or csv
    file = open(complete_name, "a", encoding="utf-8")
    return file
