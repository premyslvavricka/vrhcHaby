#třídy: zásobník, kostka?, hrací deska, hráč1 - hráč2, AI, printer

from typing import Any
import random
import gameboard
import jsonpickle

def SavePlayer(player):
    return jsonpickle.encode(player, unpicklable=True)

def LoadPlayer(data_string):
    return jsonpickle.decode(data_string)


class Player:

    def __init__(self, name, color):
        self._name = name
        self._color = color
        
    def GetName(self):
        return self._name

    def GetColor(self):
        return self._color
    
    def DoTurn(self, game_board):
        pass

class LocalPlayer(Player):

    def __init__(self, name, color):
        super().__init__(name, color)

    def DoTurn(self, game_board):
        return False

class AI(Player):

    def __init__(self, name, color):
        super().__init__(name, color)

    def DoTurn(self, game_board):
        game_board.ThrowDices()

        while(game_board.CanContinueTurn()):
            all_possible_moves = game_board.GetAllPossibleMoves()
            if game_board.IsInPrison():
                game_board.MoveStone(gameboard.PRISON, random.choice(game_board.AvailableMoves(gameboard.PRISON)))
                continue
            for idx in game_board.GetHomeArea():
                if game_board.CanScore(idx):
                    scorable = game_board.ScoreableIndexes()
                    print(scorable)
                    print(game_board.GetAvailableMoves())
                    if len(scorable) > 0:
                        game_board.MoveStone(scorable[0], gameboard.SCORE_INDEX)
                        continue

            for idx in range(len(all_possible_moves)):
                if len(all_possible_moves[idx]) != 0:
                    game_board.MoveStone(idx, random.choice(all_possible_moves[idx]))
                    break

        return True