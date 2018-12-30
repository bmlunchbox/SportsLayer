from Data import SoupService
from Data import DataDictionary


def get_stats(team):
    standings = SoupService.generate_standings()

    team_stats = []
    for sublist in standings:
        if sublist[0] == DataDictionary.nba_string[team]:
            team_stats = sublist
            break

    output = "%s (%s): are %s-%s with a %s win percentage. They are %s behind the leading team on a %s streak " \
             "(last 10: %s).\n" \
             % (team_stats[0], team_stats[1], team_stats[2], team_stats[3],
                team_stats[4], team_stats[5], team_stats[13], team_stats[14])

    return output


def get_full_stats(team):
    standings = SoupService.generate_standings()

    team_stats = []
    for sublist in standings:
        if sublist[0] == DataDictionary.nba_string[team]:
            team_stats = sublist
            break

    output = "%s (%s-%s): are %s at home, %s away, and %s in their conference. They average %s a game, " \
             "%s compared to their opponents' %s." % \
             (team_stats[0], team_stats[2], team_stats[3], team_stats[6],
              team_stats[7], team_stats[9], team_stats[10], team_stats[12], team_stats[11])

    return output
