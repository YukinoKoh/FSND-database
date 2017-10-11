#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

# import library postgresql
import psycopg2

DBNAME = 'tournament'


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(DBNAME))
        c = db.cursor()
        return db, c
    except:
        print('batabase connection failed')


def deleteMatches():
    """Remove all the match records from the database."""
    db, c = connect()
    c.execute('TRUNCATE matches CASCADE')
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db, c = connect()
    c.execute('TRUNCATE players CASCADE')
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db, c = connect()
    c.execute('SELECT count (name) FROM players')
    numPlayers = c.fetchone()
    db.close()
    return numPlayers[0]


def registerPlayer(player):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.
    Args:
      name: the player's full name (need not be unique).
    """
    db, c = connect()
    SQL = "INSERT INTO players (name) VALUES ('{0}')"
    player = player.replace("'", "''")
    c.execute(SQL.format(player,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place,
    or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = connect()
    c.execute('''CREATE VIEW results AS SELECT players.id, players.name,
                 (SELECT COUNT(matches.winner_id) FROM matches
                 WHERE matches.winner_id = players.id) AS wins,
                 (SELECT COUNT(matches.loser_id) FROM matches
                 WHERE matches.loser_id = players.id) AS loss
                 FROM players FULL OUTER
                 JOIN matches ON matches.winner_id = players.id''')
    c.execute('''SELECT id, name, wins, (wins+loss) AS matches FROM
                 results ORDER BY wins''')
    tuplesList = c.fetchall()
    db.close()
    return tuplesList


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = connect()
    SQL = 'INSERT INTO matches (winner_id, loser_id) VALUES ({0[0]},{0[1]})'
    data = (winner, loser)
    c.execute(SQL.format(data))
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    sortedList = playerStandings()
    id1 = []
    name1 = []
    id2 = []
    name2 = []
    i = 0
    for ids, name, wins, match in sortedList:
        i += 1
        if i % 2 == 1:
            id1.append(ids)
            name1.append(name)
        else:
            id2.append(ids)
            name2.append(name)
    listTuples = zip(id1, name1, id2, name2)
    return listTuples

