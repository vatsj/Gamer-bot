# Gamer-bot
framework for training RL agents to play (simple, finite) games

## Capabilities

Provides `gamer` package, which consists of the following sub-packages:

- games: finite n-player games
- players: players of a given `gamer.games` game, with policy deciding moves given the game state
- strategists: agents designed to optimize strategy for a given game; trains by producing players and having them play games

## How to run

The main file is run from the project's root directory via the following command
> python src/main.py

### Dependencies

A incomplete list is below:
- Python 3.3 and up
- reasonably up-to-date `npm`
- Python packages: numpy, scipy, chess (can be installed with `npm i numpy scipy chess`)
