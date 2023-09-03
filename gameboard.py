from random import randint
import copy
from typing import Any
import jsonpickle


class EndlessStack:
    """
    Třída slouží k reprezentování kamenů na jednotlivým políčku
    - initial_stones = list, který slouží k naplnění políčka kameny na začátku či načtení hry
    """

    def __init__(self, identity:int, initial_stones:list = []):
        self._identityInt = identity                        #ciselne oznaceni policka
        self._stones_list = initial_stones                  #seznam s kameny

        self._held_color = str                              #barva kamenu v seznamu
        self.__SetColor()


    def __SetColor(self):           #nastavuje barvu podle kamenu v seznamu
        if self.__len__() > 0:
            self._held_color = self._stones_list[0].GetColor()
        else:
            self._held_color = "None"

    def InsertIn(self, stone_to_insert):            #vklada kamen do seznamu
        self._stones_list.append(stone_to_insert)
        self.__SetColor()

    def PopOut(self):               #vyhazuje vrchni prvek seznamu
        if self.__len__() > 0:
            self.__SetColor()
            return self._stones_list.pop(self.__len__()-1)
    
    def GetAsChar(self):       #vraci pismene oznaceni policka
        return chr(97 + self._identityInt)
    
    def GetAsInt(self):       #vraci ciselne oznaceni policka
        return self._identityInt
    
    def GetHeldColor(self):     #vraci barvu kamenu v policku
        return self._held_color

    def ListList(self):         #vraci cele pole """debug"""
        return [self._stones_list[idx].GetIdentity() for idx in range(self.__len__())]

    def ListStones(self):
        return [self._stones_list[idx] for idx in range(self.__len__())]

    def __len__(self):          #vraci delku pole
        return len(self._stones_list)



class DiceBag:
    """
    Třída slouží k vygenerování náhodného hodu dvou kostky do hry
    """

    def __init__(self):
        self._dices_throw = list

    def Throw(self):
        self._dices_throw = [randint(1,6) for _ in range(2)]
        return self._dices_throw

    def GetState(self):
        return self._dices_throw
    

class Stone():

    def __init__(self, color:str, number:int, position:chr):
        self._color = color
        self._number = number
        self._history_of_movement = [("bar", position)]

    def SaveMovement(self, moved_position):
        self._history_of_movement.append((self._history_of_movement[len(self._history_of_movement)-1][1], moved_position))

    def GetColor(self):
        return self._color
    
    def GetNumber(self):
        return self._number

    def GetIdentity(self):          # debug, mozne odebrat
        return self._color + str(self._number)

    def GetHistory(self):
        return self._history_of_movement


#kameny = [Stone("white",idx+1) for idx in range(5)]
#
#zasobnik1 = EndlessStack(kameny)
#
#print(zasobnik1.ListList())
#
#a = zasobnik1.PopOut()
#
#print(a.GiveColor())
#
#print(zasobnik1.ListList())

initial_stones_placement = {0:[Stone("black", 0, 0), Stone("black", 1, 0)], 
                            1:[], 2:[], 3:[], 4:[], 
                            5:[Stone("white", 0, 5), Stone("white", 1, 5), Stone("white", 2, 5), Stone("white", 3, 5), Stone("white", 4, 5)], 
                            6:[],
                            7:[Stone("white", 5, 7), Stone("white", 6, 7), Stone("white", 7, 7)],
                            8:[], 9:[], 10:[],
                            11:[Stone("black", 2, 11), Stone("black", 3, 11), Stone("black", 4, 11), Stone("black", 5, 11), Stone("black", 6, 11)],
                            12:[Stone("white", 8, 12), Stone("white", 9, 12), Stone("white", 10, 12), Stone("white", 11, 12), Stone("white", 12, 12)],
                            13:[], 14:[], 15:[],
                            16:[Stone("black", 7, 16), Stone("black", 8, 16), Stone("black", 9, 16)],
                            17:[],
                            18:[Stone("black", 10, 18), Stone("black", 11, 18), Stone("black", 12, 18), Stone("black", 13, 18), Stone("black", 14, 18)],
                            19:[], 20:[], 21:[], 22:[],
                            23:[Stone("white", 13, 23), Stone("white", 14, 23)]}


def LoadGame(data_string):
    return jsonpickle.decode(data_string)

def SaveGame(gameboard):
    return jsonpickle.encode(gameboard, unpicklable=True)


class GameBoard:

    def __init__(self, load_game:bool = True, initial_stone_placements:dict = initial_stones_placement):

        self._board_playground = []

        self._prison_white = EndlessStack(24)
        self._prison_black = EndlessStack(25)

        self._prison = {"white": EndlessStack(24), "black": EndlessStack(25)}
            
        self.PreparePlayGround(initial_stone_placements)

        self._history = {1:[]}
        self._round = 1

        self._finish_white = [] # dictionary: { "white" : [], "black" : []}
        self._finish_black = []

        self._thrown_already = False 
        self._possible_moves = []

        self._playing = "white"

        self._rule_set = {"white": {}, "black": {}}

        self._home_area = {"white": range(0,6), "black": range(18, 24)}
        self._ace_point = {"white": 0, "black": 23}

    # init ------------
    def PreparePlayGround(self, initial_stone_placements:dict):
        for idx in range(24):
            self._board_playground.append(EndlessStack(idx,copy.copy(initial_stone_placements[idx])))

    # Bool ------------

    def IsValidMove(self, player, start_point, target_point):
        if self._board_playground[start_point].GetHeldColor() != player:
            return False
        
        if self._board_playground[target_point].GetHeldColor() != player:
            if len(self._board_playground[target_point]) > 1:
                return False

        #if self._


        return True
        #much more here


    def AllInHome(self, player):                    #check
        #area = range(6,24) if player == "white" else range(0,18)
        #return self.CheckOutsideArea(player, area)

        return self.CheckOutsideArea(player, self._home_area[player])


    def AllInAcePoint(self, player):                #check
        #area = range(1,24) if player == "white" else range(0,23)
        #return self.CheckOutsideArea(player, area)

        return self.CheckOutsideArea(player, self._ace_point[player])

    def CheckOutsideArea(self, player, area):
        for position in area:
            if player == self._board_playground[position].GetHeldColor():
                return False
        return True

    def IsInPrison(self, player):               #check
        #if player == "white":
        #    if self._prison_white.GetHeldColor() == player:
        #        return True
        #    else: return False
        #else:
        #    if self._prison_black.GetHeldColor() == player:
        #        return True
        #    else: return False

        if len(self._prison[player]) > 0:
            return True
        else:
            return False



    # game update ----------

    def AvailableMoves(self, player, start_point):
        available_area = range(0,0)
        available_moves = []
        keys = []

        if self.IsInPrison(player) == True:
            keys = self._home_area.keys().remove(player)
            available_area = self._home_area[keys[0]]           #other players home area

        elif self.AllInHome(player) == True:
            available_area = self._home_area[player] + -1       #unsure if works range() + int

        elif self.AllInAcePoint(player) == True:
            available_area = -1                                 #any move leads to finish
            #special stuff

        else:
            if player == "white":
                available_area = range(0, start_point)
            else:
                available_area = range(start_point, 24)

        for possible_move in self._possible_moves:
            if player == "white":
                if start_point - possible_move in available_area:
                    if self.IsValidMove(player, start_point, start_point - possible_move):
                        available_moves.append(start_point - possible_move)

            else:
                if start_point + possible_move in available_area:
                    if self.IsValidMove(player, start_point, start_point + possible_move):
                        available_moves.append(start_point + possible_move)




    def GetAvailableMoves(self, player, start_point):
        return self.AvailableMoves(player, start_point)




    def WinCondition(self, player):
        area = range(0,24)

        if not self.IsInPrison(player):
            if self.CheckOutsideArea(player, area):
                pass #he wins


    def __WriteHistory(self, what_to_write:str) -> None:
        self._history[self._round].append(what_to_write)

    def NextRound(self):
        self.PassTurn()
        self._round += 1

    def PassTurn(self):
        if self._playing == "white":
            self._playing == "black"

        else:
            self._playing == "white"

    def MoveStone(self, player, start_point, target_point):
        if self.IsValidMove(player, start_point, target_point):
            if self._board_playground[target_point].GetHeldColor() != "white" and len(self._board_playground[target_point]) == 1:
                self.ToPrison("black" if player == "white" else "white", target_point)
            stone_to_move = self._board_playground[start_point].PopOut()
            self._board_playground[target_point].InsertIn(stone_to_move)


    def ObtainMoves(self, player):
        if player == "white":
            self._dice_moves_white = self.ThrowDices()
        else:
            self._dice_moves_black = self.ThrowDices()

    def ThrowDices(self):
        dice_throw = DiceBag().Throw()

        if dice_throw[0] == dice_throw[1]:
            return [dice_throw[0] for _ in range(4)]
        else:
            return list(dice_throw)

    def ToPrison(self, opposing_player, point):
        stone_to_prison = self._board_playground[point].PopOut()
        if opposing_player == "white":
            self._prison_white.InsertIn(stone_to_prison)
        else:
            self._prison_black.InsertIn(stone_to_prison)
        stone_to_prison.SaveMovement("Prison")
    # Get ----------

    def GetGameSpace(self):
        listing = {}
        for point in self._board_playground:
            listing[point.GetAsInt()] = point.ListStones()
        return listing

    def GetPrison(self, player):
        return self._prison_white if player == "white" else self._prison_black

    def GetFinish(self, player):
        return self._finish_white if player == "white" else self._finish_black

    def GetHistory(self):
        return self._history

    def GetDices(self):
        return self._dice_moves

    #debug ------------

    def PrintGround(self):
        for policko in self._board_playground:
            print(f"{policko.GetAsInt()} - {policko.ListList()}")




gmbrd = GameBoard()

gmbrd.PrintGround()

gmbrd.MoveStone("white", 5, 7)

gmbrd.PrintGround()

print("---------------")
gmbrd2 = jsonpickle.decode(jsonpickle.encode(gmbrd, unpicklable=True))

gmbrd2.PrintGround()

#ston = Stone("white", 2, 0)
#ston.SaveMovement(3)
#print(ston.GetHistory())
#
#zasob = EndlessStack(1, [ston, ston])



