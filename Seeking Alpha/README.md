This program is used to open a Seeking Alpha on a firefox window using Selenium.
The Selenium script will continually scroll to the new bottom of the page for a given number of times.
This page is passed to a parser, which ascertains the links, titles, and some other metadata from each 'Article'.
Then, each of the pages at these links is parsed for the text of each 'Article'. 
This is written into a text file.

I am currently struggling with avoiding captchas and 403 errors.
I have set the headers to less recognizable ones and I have tried building a rotating proxy system to pass different IPs to Seeking Alpha.
