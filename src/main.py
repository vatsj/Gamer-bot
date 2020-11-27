# importing modules provided by this project
import gamer
import compete

# defines classes/objects for game/player
game = gamer.games.instances.T3
playerType = gamer.players.types.RandomPlayer

player_types = [playerType for i in range(game.nPlayers)]

# compete in several-game match
results = compete.compete_player(game, player_types)
print(results)

# render a game
compete.visualize(game, player_types)
