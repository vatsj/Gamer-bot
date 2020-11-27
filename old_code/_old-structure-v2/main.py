from helper import import_helper as ih

gameDir = "/src/games/TicTacToe.py"
playerDir = "/src/types/RandomPlayer.py"

game = ih(gameDir, "TicTactoe").T3
RandomPlayer = ih(playerDir, "RandomPlayer").RandomPlayer

game = Game.T3
players = []
for i in range(T3.nPlayers):
    players += RandomPlayer(game, i + 1)

nGames = 10
for i in range(nGames):
    print(game.play(players))
