# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        from math import sqrt
        scoreSum = 0 #初始化评估函数分数
        newFood = newFood.asList()
        currentFood = currentGameState.getFood().asList()
        ghostDistances = []

        #判断智能体的状态
        if successorGameState.isLose():
            return -999999999

        #使用曼哈顿距离计算幽灵与吃豆人之间的距离，并取其最小值
        for ghostPosition in successorGameState.getGhostPositions():
            ghostDistances.append(manhattanDistance(newPos,ghostPosition))
        minGhostDistances = min(ghostDistances)

        #设置危险距离
        danger = 0
        if minGhostDistances < 2:
            danger -= 9999999
        elif action == 'stop':
            return -999999

        #使用曼哈顿距离计算吃豆人与豆子之间的距离
        totalFoodDistance = 0
        averageFoodDistance = 0
        FoodDistance = []
        if newFood:
            for food in newFood:
                totalFoodDistance += sqrt(float(manhattanDistance(newPos,food) + 2.0))
                FoodDistance.append(sqrt(float(manhattanDistance(newPos,food) + 1.0)))
            averageFoodDistance = totalFoodDistance / len(newFood)

        minFoodDistance = 0
        if FoodDistance:
            minFoodDistance += min(FoodDistance)

        scoreChange = successorGameState.getScore() - currentGameState.getScore()

        #设置无敌时间分数，处于无敌时间时，吃豆人不畏惧幽灵
        strongeTime = 0
        for time in newScaredTimes:
            strongeTime += time

        eat = 0
        if newPos in currentFood:
            eat += 9999999

        #设置评估分数值，分值越低，吃豆人越谨慎
        scoreSum += eat + danger + strongeTime - 2*minFoodDistance - 2*averageFoodDistance + 0.2*minGhostDistances + scoreChange
        return scoreSum

        #return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        n = gameState.getNumAgents() # 返回吃豆人和幽灵的数量
        Depth = self.depth # 返回此轮游戏的深度

        # 自定义一个minimax函数，输入值分别是状态、深度、当前深度、以及数量（吃豆人+幽灵的数量）
        def minmax(state, Depth, currentDepth = -1, number = n):
            currentDepth += 1 # 每次执行minimax函数当前深度+1

            # 判断当前状态是否为游戏结束的状态
            if Depth * n == currentDepth or state.isLose() or state.isWin():
                return self.evaluationFunction(state), "stop"

            # minimax
            if currentDepth % n == 0:
                maxValue = -999999
                move = ""

                for action in state.getLegalActions(0):
                    value = minmax(state.generateSuccessor(0,action),Depth,currentDepth,number)[0]
                    if value > maxValue:
                        maxValue = value
                        move = action
                return maxValue, move

            else:
                index = currentDepth % n
                minValue = 999999

                for action in state.getLegalActions(index):
                    value = minmax(state.generateSuccessor(index,action),Depth,currentDepth,number)[0]
                    if value < minValue:
                        minValue = value
                return minValue, " "

        return minmax(gameState,Depth,-1,n)[1]
        # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        Depth = self.depth # 返回此轮游戏的深度
        n = gameState.getNumAgents()

        def alphabetaMax(gamestate, currentDepth, alpha, beta):
            actions_for_pacman = gamestate.getLegalActions(0)

            if currentDepth > self.depth or gamestate.isWin() or not actions_for_pacman:
                return self.evaluationFunction(gamestate), Directions.STOP

            maxValue = float('-inf')
            bestAction = Directions.STOP
            for action in actions_for_pacman:
                successor = gamestate.generateSuccessor(0, action)
                value = alphabetaMin(successor, 1, currentDepth, alpha, beta)[0]
                if value > maxValue:
                    maxValue = value
                    bestAction = action
                if maxValue > beta:
                    return maxValue, bestAction
                alpha = max(alpha, maxValue)

            return maxValue, bestAction

        def alphabetaMin(gamestate, index, currentDepth, alpha, beta):
            actions_for_ghost = gamestate.getLegalActions(index)
            if not actions_for_ghost or gamestate.isLose():
                return self.evaluationFunction(gamestate), Directions.STOP

            minValue = float('inf')
            bestAction = Directions.STOP
            isPacman = index == n - 1
            for action in actions_for_ghost:
                successor = gamestate.generateSuccessor(index, action)
                if isPacman:
                    value = alphabetaMax(successor, currentDepth + 1, alpha, beta)[0]
                else:
                    value = alphabetaMin(successor, index + 1, currentDepth, alpha, beta)[0]

                if value < minValue:
                    minValue = value
                    bestAction = action
                if minValue < alpha:
                    return minValue, bestAction
                beta = min(beta, minValue)

            return minValue, bestAction


        defaultAlpha = float('-inf')
        defaultBeta = float('inf')
        return alphabetaMax(gameState, Depth, defaultAlpha, defaultBeta)[1]
        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
