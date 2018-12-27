from Data import SoupService
from Data import DataDictionary


# return the next games in schedule
# input: team name (string) and number of games queried (int)
# output: user string (string)
def get_next_schedule(team, num):
    SoupService.generate_schedule(team)
    upcoming_games = SoupService.upcoming_games

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


# return the past game results
# input: team name (string) and number of games queried (int)
# output: user string (string)
def get_past_games(team, num):
    SoupService.generate_schedule(team)
    played_games = SoupService.played_games

    if not num:
        last_game = played_games[-1]

        location, opponent = __process_name(last_game[1])
        result, score = __process_score(last_game[2])

        return "The last game was a %s %s at %s against %s on %s." % (score, result, location, opponent, last_game[0])

    else:
        output = "Past %i game scores:\n" % num
        counter = len(played_games)-1
        for i in range(num):
            location, opponent = __process_name(played_games[counter][1])
            result, score = __process_score(played_games[counter][2])

            output += "%s: %s %s against %s at %s.\n" % (played_games[counter][0], score, result, opponent, location)
            counter -= 1

        return output


# sanitizes string and parses into opponent and home/away
# input: scraped string
# output: opponent and home court location
def __process_name(text):

    if "@" in text:
        location = "away"
    else:
        location = "home"

    opponent = DataDictionary.short_names[" ".join(text.split()[1:]).strip().lower()]

    return location, opponent


# sanitizes score and parses into game results
# input: scraped string in form of w###-###ot
# output: result and score
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
