"""
compete.py

provides helper functions to simulate competitions
among players/strategists for a given game

used through main.py to test players/strategists
"""

# player_types: array of player-type
# ex: [randomPlayer, randomPlayer]
def compete_player(game, player_types, nGames = 100):

    # instantiates players from player_types
    players = []
    for i in range(player_types):
        players.append(player_types[i](game, i + 1))

    nGames = 10
    for i in range(nGames):
        print(game.play(players))
