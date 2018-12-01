# script code:
def script(url):
    import bs4
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page = soup(page_html, "html.parser")
    return page


script("https://8102.bandcamp.com/album/2018")
