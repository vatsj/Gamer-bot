# produces an ObserverPlayer capable of playing games
  # the TrainerPlayer can (indirectly) update trainingParams
  def getTrainerPlayer(self, turnNum):

      # ObserverPlayeris has strategist set to self (this class instance)
      TP = self.players.Player(self.game, turnNum, self)

      def makeMove(gameState):
          return self.getTrainerMove(TP, gameState, turnNum, self.trainingParams)

      TP.makeMove = makeMove
      return TP

  # produces moves for TrainerPlayers based on player and trainingParams
  def getTrainerMove(self, tp, gameState, turnNum, trainingParams):
      """instance-specific method"""
      pass

  # canonical methods for TrainerPlayer observing move, result
  # can store information through access to player
  def observeTrainerMove(self, player, gameState, turnNum, move):
      """instance-specific method"""
      pass

  def observeTrainerResult(self, player, gameState, winner):
      """instance-specific method"""
      pass

  # produces the player using the strategist's "optimal strategy"
  # plays in terms of getOptimalMove
  def getOptimalPlayer(self, turnNum):
      # only have access to ObserverPlayer class
      OP = self.players.Player(self.game, turnNum)

      def makeMove(gameState):
          return self.getOptimalMove(gameState, turnNum, self.trainingParams)

      OP.makeMove = makeMove
      return OP

  # produces optimal move for a given gameState
  # only a function of gameState, trainingParams
  def getOptimalMove(self, gameState, turnNum, trainingParams):
      """instance-specific method"""
      pass
