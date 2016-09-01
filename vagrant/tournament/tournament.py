#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB=connect()
    c=DB.cursor()
    c.execute("update game set wins = 0, matches = 0")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB=connect()
    c=DB.cursor()
    c.execute("delete from game")
    DB.commit()
    DB.close()
     

def countPlayers():
    """Returns the number of players currently registered."""
    DB=connect()
    c=DB.cursor()
    c.execute("select count(id) from game ")
    count=c.fetchall()[0][0]
    DB.close()
    
    return count
    

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB=connect()
    c=DB.cursor()
    c.execute("insert into game(name) values (%s)",(name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB=connect()
    c=DB.cursor()
    c.execute("select id, name, wins,matches from game order by wins DESC")
    res=c.fetchall()
    DB.close()
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB=connect()
    c=DB.cursor()
    c.execute("select wins from game where id = {0}".format(winner))
    winner_wins=c.fetchall()[0][0]+1
    c.execute("select matches from game where id = {0}".format(winner))
    winners_matches=c.fetchall()[0][0]+1
    c.execute("select matches from game where id = {0}".format(loser))
    loser_matches=c.fetchall()[0][0]+1
    c.execute("update game set wins={0}, matches={1} where id= {2}".format(winner_wins,winners_matches,winner))
    c.execute("update game set matches={0} where id= {1}".format(loser_matches,loser))
    
    DB.commit()
    DB.close()
    
    
    
 
 
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
    
    playerslist=playerStandings() # list of tuples(id,name,wins,matches)
    resList=[]
    count=0
    total=countPlayers()
    while (count<total):
        id1=playerslist[count][0]
        name1=playerslist[count][1]
        count=count+1
        id2=playerslist[count][0]
        name2=playerslist[count][1]
        resList.append((id1,name1,id2,name2))
        count=count+1
    return resList
        
    
    
    
    
    
    
    
    
    
    
    
    


