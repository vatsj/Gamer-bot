import gamer

# defines classes/objects for game/player
game = gamer.games.instances.T3
playerType = gamer.players.types.RandomPlayer

players = []
for i in range(game.nPlayers):
    players.append(playerType(game, i + 1))

nGames = 10
for i in range(nGames):
    print(game.play(players))

# render a game
game.play(players, True)
