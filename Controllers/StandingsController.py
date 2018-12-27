from Data import SoupService
from Data import DataDictionary
from operator import itemgetter


def get_conference_standings(conference):
    standings = SoupService.generate_standings()
    output = ""

    if conference.lower() == "eastern":
        standings = standings[0:15]
    elif conference.lower() == "western":
        standings = standings[15:30]

    for team in standings:
        output += "%s: %s (%s-%s)\n" % (team[1], team[0], team[2], team[3])

    return output


def get_all():
    standings = SoupService.generate_standings()
    output = ""

    sorted_list = sorted(standings, key=itemgetter(4), reverse=True)

    for i, team in enumerate(sorted_list):
        output += "%i: %s (%s-%s)\n" % (i+1, team[0], team[2], team[3])

    return output


def get_playoff_teams(conference):
    standings = SoupService.generate_standings()
    output = ""

    if conference.lower() == "eastern":
        standings = standings[0:8]
    elif conference.lower() == "western":
        standings = standings[15:21]

    length = int(len(standings))-1
    for i in range(4):
        output += "%s (%s) - %s (%s)\n" % (standings[i][0], standings[i][1],
                                           standings[length-i][0], standings[length-i][1])

    return output


def get_team(team):
    standings = SoupService.generate_standings()

    team_stats = []
    for sublist in standings:
        if sublist[0] == DataDictionary.nba_string[team]:
            team_stats = sublist
            break

    output = "%s (%s): %s wins, %s losses" % (team_stats[0], team_stats[1], team_stats[2], team_stats[3])

    return output

# to do note: cache on the client side
