"""
compete.py

provides helper functions to simulate competitions
among players/strategists for a given game

used through main.py to test players/strategists
"""

from collections import defaultdict

# players play game
# helper method for other compete fns
def compete(game, players, nGames):

    # simulate games
    results_dict = defaultdict(lambda: 0)
    for i in range(nGames):
        result = game.play(players)
        results_dict[result] += 1

    # normalize results
    for key in results_dict:
        results_dict[key] = round(results_dict[key] / nGames, 2)

    return results_dict

# helper function to convert between
# player_types --> players
def pt2p(game, player_types):
    # instantiates players from player_types
    players = []
    for i in range(game.nPlayers):
        players.append(player_types[i](game, i + 1))

    return players

# player_types: array of player-type
# ex: [randomPlayer, randomPlayer]
def compete_player(game, player_types, nGames = 100):

    players = pt2p(game, player_types)

    return compete(game, players, nGames)

# strategist_types: array of types ((sub)classes) of strategist
def compete_strategist(game, strategist_types, nGames = 100):

    TRAINING_TIME = 10**4

    # instantiates from strategist_types
    # strategists = []
    # for i in range(game.nPlayers):
    #     strategists.append(strategist_types[i](game, i + 1))

    strategists = pt2p(game, strategist_types)

    # generates optimal players from strategists
    players = [s.getOptimalPlayer() for s in strategists]

    return compete(game, players, nGames)

# plays a single game with board posns rendered
def visualize(game, player_types):

    # let fn accept different kinds of types for players arr?

    # instantiates players from player_types
    # players = []
    # for i in range(game.nPlayers):
    #     player_def = player_defs[i]
    #
    #     if hasattr(player_def, "makeMove"):
    #         players.append(player_def)
    #     players.append(player_types[i](game, i + 1))
    #
    # return compete(game, players, nGames)

    players = pt2p(game, player_types)
    game.play(players, render = True)
