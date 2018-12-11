# import libraries
import urllib.request
import DataDictionary
from bs4 import BeautifulSoup


base_url = "http://www.espn.com/"


# default to return next game: team, game
# input: team name as a string
# input: start will be an integer indicating how many past games
# input: end will be in integer indicating how many future games
def get_schedule(team, start, end):
    schedule = []

    team_code = DataDictionary.team_codes.get(team)

    # generate the url
    page_url = base_url + 'nba/team/schedule/_/name/'
    page_url += str(team_code)

    # create the request
    page = urllib.request.urlopen(page_url).read()

    # gather the html -- formatted
    soup = BeautifulSoup(page, 'html.parser')

    # go through the table and grab dates, opponent, score or time
    for tr in soup.find_all('tr')[4:]:
        tds = tr.find_all('td')

        schedule.append([tds[0].text, tds[1].text.strip('vs@ '), tds[2].text.strip()])

    for line in schedule:
        print(str(line) + "\n")


get_schedule('torontoraptors', None, None)
