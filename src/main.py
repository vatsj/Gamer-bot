# importing modules provided by this project
import gamer
import compete

# defines classes/objects for game/player
game = gamer.games.instances.T3
playerType = gamer.players.types.RandomPlayer
ObserverPlayer = gamer.players.types.RandomPlayer
strategistType = gamer.strategists.types.MonteCarlo
strategistType.ObserverPlayer = ObserverPlayer

player_types = [playerType for i in range(game.nPlayers)]
s_types = [strategistType for i in range(game.nPlayers)]

# compete in several-game match
# results = compete.compete_player(game, player_types)
results = compete.compete_strategist(game, s_types)
print(results)

# render a game
compete.visualize(game, player_types)
