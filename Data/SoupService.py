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
    team_tracker = []

    url = "http://www.espn.com/nba/standings"
    page = urllib.request.urlopen(url)

    soup = BeautifulSoup(page, 'html.parser')

    # find the table containing the team names
    rows = soup.find_all("span", {"class": "hide-mobile"})

    rank = 1

    # for each entry in the table
    for row in rows:
        # get the team name
        team = row.contents[0].string

        # if it has already been entered
        if team not in team_tracker:
            # enter it into the list and the tracker
            standings.append([team, rank])
            team_tracker.append(team)

            # increase or reset rank
            if rank == 15:
                rank = 1
            else:
                rank += 1

    # grab all the stats in the table
    stats = soup.find_all("span", {"class": "stat-cell"})

    # extract from html
    processed = []
    for s in stats:
        processed.append(s.contents[0])

    # bundle them by team
    index = 0
    for i in range(0, len(processed), 13):
        standings[index].extend(processed[i:i + 13])
        index += 1

    # list of lists where each list is a bundle of a team's stats
    # structure:
    # [team, rank, wins, losses, percentage, home_rec, away_rec, div_rec, con_rec, ppg, opp_ppg, pt_diff, streak, L10]
    return standings


def generate_roster(team):
    roster = []
    url = "http://www.espn.com/nba/team/roster/_/name/tor"


def generate_injuries(team):
    injuries = []
    url = "http://www.espn.com/nba/team/injuries/_/name/tor"


def generate_depth(team):
    depth = []
    url = "http://www.espn.com/nba/team/depth/_/name/tor"


# on the urllib.request.urlopen(url)
# urllib.error.URLError: <urlopen error [Errno 11001] getaddrinfo failed>
# should package as JSON either here or in controllers
