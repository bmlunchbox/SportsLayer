# import libraries
import urllib.request
import DataDictionary
from bs4 import BeautifulSoup


base_url = "http://www.espn.com/"
played_games = []
upcoming_games = []


# default to return next game: team, game
# input: team name as a string
# output: list of lists containing: date, opponent, score/date
def generate_schedule(team):
    global played_games, upcoming_games
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

        schedule.append([tds[0].text, tds[1].text.strip('@vs '), tds[2].text.strip()])

    for i, game in enumerate(schedule):
        if game[0].lower() == 'date':
            played_games = schedule[:i]
            upcoming_games = schedule[i+1:]
            break


# return next or past x games
def get_next_schedule(team, next):
    global upcoming_games

    if not upcoming_games:
        generate_schedule(team)

    if not next:
        next_game = upcoming_games[0]
        return "\nThe next game will be on %s against the %s at %s." % (next_game[0], next_game[1], next_game[2])
    else:
        pass


print(get_next_schedule('torontoraptors', None))
