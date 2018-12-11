# import libraries
import urllib.request
from bs4 import BeautifulSoup

soup = BeautifulSoup(html_doc, 'html.parser')

teams = {
    'torontoraptors': 'tor',
    'bostonceltics': 'bos',
    'dallasmavericks': 'dal'
}

# http request
pageUrl = 'http://www.espn.com/nba/team/schedule/_/name/tor'
page = urllib.request.urlopen(pageUrl)

# text file
file = open("test.txt", "w")

file.write(str(page.read()))
