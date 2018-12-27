import time
from bs4 import BeautifulSoup
import open_functions as of
import selenium.webdriver as wd

root_url = "https://seekingalpha.com"

profile = wd.FirefoxProfile()
profile.set_preference("general.useragent.override", "Mozilla/5.0")


class CompanyGrab:
    def __init__(self, url_ext, file_name):
        self.driver = wd.Firefox(profile)
        self.driver.implicitly_wait(30)
        self.base_url = root_url
        self.url_ext = url_ext
        # self.data = None;
        self.file_name = file_name
        self.verificationErrors = []
        self.accept_next_alert = True

    def grab_execute(self):

        file = of.open_file(self.file_name, "csv")
        driver = self.driver

        delay = 1.5
        driver.get(self.base_url + self.url_ext)

        for i in range(1, 3):  # usually 350
            print(str(i) + "\n")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(delay)

        html_source = driver.page_source
        data = html_source.encode('utf-8')
        parse_file_for_links(data, file, self.file_name)  # arg 1 was data
        file.close()
        return data


# article name convention eg MSFT + (article num) 0 + date of article

def get_article_text(url, a_file_name):

    page = of.proxy_open(url)
    file = of.open_file(a_file_name, "txt")

    content = page.find("div", {"id": "main_content"})

    if content is None:

        article = content.div.article

        summary = article.find("div", {"class": "article-summary article-width"}).text
        all_text = article.find("div", {"class": "sa-art article-width"}).text

        header = article.header
        text = article.div

        print(str(header) + "\n")
        print(str(summary) + "\n")
        print(str(text) + "\n")

        # write to file
        file.write(str(summary) + "\n")
        file.write(str(all_text))

    else:
        # if beautiful soup doesnt work, handle with selenium
        print("captcha error most likely")

        file.write("captcha error most likely \n")
        file.write(str(time.time))

    file.close()


def parse_file_for_links(data, file, company):

        page = BeautifulSoup(data, "html.parser")
        container = page.find("div", {"class": "content_block_investment_views"}).ul

        articles = container.find_all("li")
        number = 0

        for li in articles:

            # write each article title (maybe replace commas, maybe write this as a text file since its not a table
            datas = li.find_all("div")
            item = datas[1].find_all("div")

            info = item[0].a
            title = info.text

            # remove commas from title
            url = root_url + info['href']
            author_url = item[1].a['href']

            context = item[1].text.strip().split("•")

            author = context[0]
            date = context[1]

            comments = context[2]
            comment_count = comments.split("\xa0")[0]

            file_name = company + "_" + str(number) + "_" + date
            get_article_text(url, file_name)

            file.write(str(number) + "\n")


            print(url)
            print("Article Number: " + str(number) + "\n")

            number += 1
            time.sleep(1.5)


# test
AMZN = CompanyGrab("/symbol/AMZN?s=amzn", "AMZN")
AMZN.grab_execute()
