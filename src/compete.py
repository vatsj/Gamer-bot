"""
compete.py

provides helper functions to simulate competitions
among players/strategists for a given game

used through main.py to test players/strategists
"""

from collections import defaultdict
import random

# helper function to convert between
# player_types --> players
def pt2p(game, player_types):
    # instantiates players from player_types
    players = []
    for i in range(game.nPlayers):
        players.append(player_types[i](game, i + 1))

    return players

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

# plays a single game with board posns rendered
def visualize(game, player_types):

    players = pt2p(game, player_types)
    game.play(players, render = True)

# player_types: array of player-type
# ex: [randomPlayer, randomPlayer]
def compete_player(game, player_types, nGames = 100):

    players = pt2p(game, player_types)

    return compete(game, players, nGames)

# strategist_types: array of types ((sub)classes) of strategist
def compete_strategist(game, strategist_types, nGames = 100):

    # small training time for bug-checking
    TRAINING_TIME = 10**5

    # instantiates from strategist_types
    # strategists = []
    # for i in range(game.nPlayers):
    #     strategists.append(strategist_types[i](game, i + 1))

    strategists = pt2p(game, strategist_types)

    # generates optimal players from strategists
    players = []
    for s in strategists:
        s.train(TRAINING_TIME)
        players.append(s.getOptimalPlayer())

    # visualize a single game
    game.play(players, render = True)

    results = compete(game, players, nGames)
    return results

def analyze_strategist(game, strategist, InputPlayer):

    # assigns modifiers to strategist
    strategist.modifiers["memo"] = True
    strategist.modifiers["GTA"] = True

    # small training time for bug-checking
    TRAINING_TIME = 10**3
    strategist.train(TRAINING_TIME)
    strategist.render = True

    play = input("Would you like to play against the trained strategist? ([y]/n)")
    while not(play.lower() == "n"):

        # constructs players in random order
        players = []
        order = [i for i in range(game.nPlayers)]
        random.shuffle(order)
        for i in range(game.nPlayers):
            if order[i] == 0:
                players.append(InputPlayer(game, i + 1))
            else:
                curr_OP = strategist.getOptimalPlayer(i + 1)
                # signals the player to render info about chosen moves
                # curr_OP.render = True
                players.append(curr_OP)

        # plays game, prompts to play again
        game.play(players, render=True)

        play = input("Play again? ([y]/n)")
