import Gamer

# defines classes/objects for game/player
game = Gamer.games.instances.T3
playerType = Gamer.players.instances.RandomPlayer

players = []
for i in range(T3.nPlayers):
    players += playerType(game, i + 1)

nGames = 10
for i in range(nGames):
    print(game.play(players))
