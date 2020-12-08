# importing modules provided by this project
import gamer
import compete

# defines classes/objects for game/player
game = gamer.games.instances.T3
# game = gamer.games.instances.KTChess

playerType = gamer.players.types.RandomPlayer
InputPlayer = gamer.players.types.InputPlayer

strategistType = gamer.strategists.types.MonteCarlo
strategistType.players = gamer.players

player_types = [playerType for i in range(game.nPlayers)]
s_types = [strategistType for i in range(game.nPlayers)]

# compete in several-game match
# results = compete.compete_player(game, player_types)
# results = compete.compete_strategist(game, s_types)
# print(results)

# render a game
# compete.visualize(game, player_types)

# trains and interacts with a strategist
compete.analyze_strategist(game, strategistType(game), InputPlayer)
