from Data import SoupService


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
    return ""


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
    return ""
