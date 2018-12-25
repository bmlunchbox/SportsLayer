# import libraries
import urllib.request
from Data import DataDictionary
from bs4 import BeautifulSoup


upcoming_games = []
played_games = []


# get the team schedule and store it locally
# input: team name as a string
# output: none
def generate_schedule(team):
    global played_games, upcoming_games
    schedule = []

    team_code = DataDictionary.team_codes.get(team)

    # generate the url
    page_url = 'http://www.espn.com/nba/team/schedule/_/name/' + str(team_code)

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


def generate_standings():
    standings = []
    tracker = []

    url = "http://www.espn.com/nba/standings"
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')

    for tr in soup.find_all('tr'):
        # find the table containing the team names
        rows = tr.find_all("span", {"class": "hide-mobile"})

        rank = 1

        # for each entry in the table
        for row in rows:
            # get the team name
            team = row.contents[0].string

            # if it has already been entered
            if team not in tracker:
                # enter it into the list and the tracker
                standings.append([team, rank])
                tracker.append(team)

                # increase or reset rank
                if rank == 15:
                    rank = 1
                else:
                    rank += 1

        stats = tr.find_all("span", {"class": "stat-cell"})
        temp = []
        counter = 0
        for s in stats:
            if counter > 12:
                print(temp)
                counter = 0
                del temp[:]

            temp.append(s.contents[0])
            counter += 1


