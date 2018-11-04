# scraping

I wrote a program using BeautifulSoup and Python that will parse an artists bandcamp and retrieve
all of the song lengths, titles, and the 'about track' and 'track credits tab'

There are two bugs that I know of: 
  - The utf-8 encoding is needed (getting some errors otherwise), however it seems to corrupt or misinterpret some text.
  - I am not parsing the track credits text correctly. I am splitting by commas, however, the second comma comes before the year, so the year of album upload is put into every track credits section.
  
  **HOw TO RUN:**
  You will need beautiful soup and python.
  Run the script out of convienience if you like.
  Then edit the bandcamp_grab file to make a call to the bandcamp site that you want.
  
  
