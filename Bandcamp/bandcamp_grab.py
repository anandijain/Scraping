import os.path
import bs4

from open_functions import open_page
from open_functions import open_file
from album_grab import album_grab


def bandcamp_grab(url_to_grab, file_name):
    # grabs the titles and lengths of songs from a bandcamp
    # stores data in csv
    page = open_page(url_to_grab)
    data = page.find("div", {"class": "leftMiddleColumns"}).ol.find_all("li")
    for li in data:
        incomplete_album_link = li.find('a', href=True)
        if incomplete_album_link is not None:
            url_album = url_to_grab + incomplete_album_link['href']
            album_grab(url_album, file_name)


# bandcamp_grab("https://8102.bandcamp.com", "bandcamp_status_11_3_2018")
