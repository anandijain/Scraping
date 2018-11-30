import os.path
import bs4

from open_functions import open_page
from open_functions import open_file
from song_grab import song_grab


def album_grab(url_to_grab, file_name):

    # grabs the titles and lengths of songs from a bandcamp
    # stores data in csv
    page = open_page(url_to_grab)
    album = page.find_all("tr", {"itemprop": "tracks"})
    track_number = 1
    # add album name write and track number
    for track in album:
        local_url = track.find("a", {"itemprop": "url"})['href']
        song_url = "https://8102.bandcamp.com" + local_url
        # song grab actually writes to the csv, this simply calls it.
        song_grab(song_url, file_name, track_number)
        track_number += 1


"""

https: // 8102.
bandcamp.com / album / 2018

"""
