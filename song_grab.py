import os.path
import bs4

from open_functions import open_page
from open_functions import open_file


def song_grab(url, file_name, track_num):
    page = open_page(url)
    file = open_file(file_name)

    song_name = page.find("h2", {"class": "trackTitle"}).text.strip()
    abt_divfind = page.find("div", {"class": "tralbumData tralbum-about"})
    if abt_divfind is not None:
        abt_text = abt_divfind.text
        abt = ' '.join(abt_text.split())
    else:
        abt = ""
    track_creds = page.find("div", {"class": "tralbumData tralbum-credits"})
    if track_creds is not None:
        creds_text = track_creds.text
        creds2 = ' '.join(creds_text.split())
        creds = creds2.split(",")[2]
    song_duration = page.find("meta", {"itemprop": "duration"})['content']
    write_string = str(track_num) + ", " + song_name + ", " + song_duration + ", " + abt + ", " + creds + "\n"
    # is it better to do one write all at once, maybe dont want 'abt' to add a new line for example
    file.write(write_string)
    file.close()

