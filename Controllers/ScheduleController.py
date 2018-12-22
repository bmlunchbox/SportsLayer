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
        location, opponent = __process_name(next_game[1])

        return "\nThe next game is on %s against %s (%s) at %s." % (next_game[0], opponent, location, next_game[2])

    else:
        output = "Next %i games:\n" % num
        for i in range(num):
            location, opponent = __process_name(upcoming_games[i][1])
            output += "%s: %s game against %s at %s.\n" % (upcoming_games[i][0], location, opponent,
                                                           upcoming_games[i][2])
        return output


def get_past_games(team, num):
    global played_games

    if not played_games:
        generate_schedule(team)

    if not num:
        last_game = played_games[-1]

        location, opponent = __process_name(last_game[1])
        result, score = __process_score(last_game[2])

        return "The last game was a %s %s at %s against %s on %s." % (score, result, location, opponent, last_game[0])

    else:
        output = "Past %i game scores:\n" % num
        counter = len(played_games) - 1
        for i in range(num):
            location, opponent = __process_name(played_games[counter][1])
            result, score = __process_score(played_games[counter][2])

            output += "%s: %s %s against %s at %s.\n" % (played_games[counter][0], score, result, opponent, location)
            counter -= 1

        return output


# sanitizes string and parses into opponent and home/away
# input: scraped string
# output: opponent and if it's home or away
def __process_name(text):

    if "@" in text:
        location = "away"
    else:
        location = "home"

    opponent = DataDictionary.short_names[" ".join(text.split()[1:]).strip().lower()]

    return location, opponent


def __process_score(text):
    overtime = ''

    if text[-2:-1].lower() == 'ot':
        overtime = 'overtime '

    if text[0].lower() == 'w':
        result = overtime + 'win'
    else:
        result = overtime + 'loss'

    score = text[1:]

    return result, score


print(get_past_games("toronto", None))
# print("\n")
print(get_past_games("toronto", 4))


# todo: unit test functions - especially the scrape call (expected output vs output)
# todo: next up create something to access these controllers
# todo: save the schedule in a database
