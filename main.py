from helper import import_helper as ih

gameDir = "/src/games/TicTactoe.py"
playerDir = "/src/types/RandomPlayer.py"

game = ih(gameDir, "TicTactoe").T3
RandomPlayer = ih(playerDir, "RandomPlayer").RandomPlayer

game = Game.T3
players = []
for i in range(T3.nPlayers):
    players += RandomPlayer(game)
