# script code:
def script(url):
    import requests
    from bs4 import BeautifulSoup
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = requests.get(url, headers=headers)
    page_html = req.text
    page = BeautifulSoup(page_html, "html.parser")
    return page
