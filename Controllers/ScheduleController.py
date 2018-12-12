# import libraries
import urllib.request
from Data import DataDictionary
from bs4 import BeautifulSoup


base_url = "http://www.espn.com/"
played_games = []
upcoming_games = []


# get the team schedule and store it locally
# input: team name as a string
# output: none
def generate_schedule(team):
    global played_games, upcoming_games, base_url
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

        schedule.append([tds[0].text, tds[1].text.strip(), tds[2].text.strip()])

    # process the raw list into played and upcoming games
    for i, game in enumerate(schedule):
        if game[0].lower() == 'date':
            played_games = schedule[:i]
            upcoming_games = schedule[i+1:]
            break


# return the next few games as a user string
# input: team name (string) and number of games queried (int)
# output: user string (string)
def get_next_schedule(team, num):
    global upcoming_games

    # if not already called, generate schedule
    if not upcoming_games:
        generate_schedule(team)

    # by default will return the next game
    if not num:
        next_game = upcoming_games[0]
        location, opponent = __process_string(next_game[1])

        return "\nThe next game is on %s against %s (%s) at %s." % (next_game[0], opponent, location, next_game[2])
    else:
        output = "Next %i games:\n" % num
        for i in range(num):
            location, opponent = __process_string(upcoming_games[i][1])
            output += "%s: %s game against %s at %s.\n" % (upcoming_games[i][0], location, opponent,
                                                           upcoming_games[i][2])

        return output


# sanitizes string and parses into opponent and home/away
# input: scraped string
# output: opponent and if it's home or away
def __process_string(text):

    if "@" in text:
        location = "away"
    else:
        location = "home"

    opponent = DataDictionary.short_names[" ".join(text.split()[1:]).strip().lower()]

    return location, opponent


print(get_next_schedule('toronto', None))
print("\n")
print(get_next_schedule('toronto', 3))
