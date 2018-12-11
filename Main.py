# import libraries
import urllib.request
import DataDictionary
from bs4 import BeautifulSoup


# check schedule
def get_schedule(team, start, end):
    # will be passed in as a query
    team_code = DataDictionary.teamCodes.get(team)

    # http request
    page_url = 'http://www.espn.com/nba/team/schedule/_/name/'
    page_url += str(team_code)

    page = urllib.request.urlopen(page_url)

    soup = BeautifulSoup(page.read(), 'html.parser')

    print(soup.prettify())


get_schedule("torontoraptors", None, None)

# soup = BeautifulSoup(html_doc, 'html.parser')

# test file
# file = open("test.txt", "w")

# file.write(str(page.read()))
