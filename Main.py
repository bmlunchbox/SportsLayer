# import libraries
import urllib.request
import DataDictionary
from bs4 import BeautifulSoup


base_url = "http://www.espn.com/"


# default to return next game: team, game
# input: team name as a string
# output: list of lists containing: date, opponent, score/date
def generate_schedule(team):
    schedule = []
    played_games = []
    upcoming_games = []

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

        schedule.append([tds[0].text, tds[1].text.strip('@vs '), tds[2].text.strip()])

    for i, game in enumerate(schedule):
        if game[0].lower() == 'date':
            played_games = schedule[:i]
            upcoming_games = schedule[i+1:]
            break

    return played_games, upcoming_games


# return next or past x games
def get_schedule(team, start, end):

    played_games, upcoming_games = generate_schedule(team)

    for game in played_games:
        print(str(game) + "\n")

    print("\n\n\n\n")

    for game in upcoming_games:
        print(str(game) + "\n")



get_schedule('torontoraptors', None, None)
