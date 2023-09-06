from random import randint
import copy
from typing import Any
import jsonpickle



class Stone():

    def __init__(self, color:str, number:int, position:chr):
        self._color = color
        self._number = number
        self._history_of_movement = [("bar", position)]
        #print(f"{self.GetIdentity()}: {self._history_of_movement}")

    def SaveMovement(self, moved_position):
        self._history_of_movement.append((self._history_of_movement[len(self._history_of_movement)-1][1], moved_position))
        #print(f"{self.GetIdentity()}: {self.GetHistory()}")

    def GetColor(self):
        return self._color
    
    def GetNumber(self):
        return self._number

    def GetIdentity(self):          # debug, mozne odebrat
        return self._color + str(self._number)

    def GetHistory(self):
        return self._history_of_movement



class EndlessStack:
    """
    Třída slouží k reprezentování kamenů na jednotlivým políčku
    - initial_stones = list, který slouží k naplnění políčka kameny na začátku či načtení hry
    """

    def __init__(self, identity:int, initial_stones:list):
        self._identityInt = identity                        #ciselne oznaceni policka
        self._stones_list = initial_stones                  #seznam s kameny

        self._held_color = str                              #barva kamenu v seznamu
        self.__SetColor()


    def __SetColor(self):           #nastavuje barvu podle kamenu v seznamu
        if self.__len__() > 0:
            self._held_color = self._stones_list[0].GetColor()
        else:
            self._held_color = "None"

    def InsertIn(self, stone_to_insert:Stone):            #vklada kamen do seznamu
        self._stones_list.append(stone_to_insert)
        stone_to_insert.SaveMovement(self.GetAsInt())
        self.__SetColor()

    def PopOut(self):               #vyhazuje vrchni prvek seznamu
        if self.__len__() > 0:
            self.__SetColor()
            return self._stones_list.pop(self.__len__()-1)
    
    def GetAsChar(self):       #vraci pismene oznaceni policka
        return chr(65 + self._identityInt)
    
    def GetAsInt(self):       #vraci ciselne oznaceni policka
        return self._identityInt
    
    def GetHeldColor(self):     #vraci barvu kamenu v policku
        return self._held_color

    def ListList(self):         #vraci cele pole """debug"""
        return [self._stones_list[idx].GetIdentity() for idx in range(self.__len__())]

    def ListStones(self):       #vraci pole kamenu
        return [self._stones_list[idx] for idx in range(self.__len__())]

    def __len__(self):          #vraci delku pole
        return len(self._stones_list)
    
    def CountByColor(self , color):
        count = 0
        for stone in self._stones_list:
            if stone.GetColor() == color:
                count += 1
        return count



class DiceBag:
    """
    Třída slouží k vygenerování náhodného hodu dvou kostky do hry
    """

    def __init__(self):
        self._dices_throw = self.Throw()

    def Throw(self):
        self._dices_throw = [randint(1,6) for _ in range(2)]
        return self._dices_throw

    def GetState(self):
        return self._dices_throw
    

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


PRISON = -5
SCORE_INDEX = -6

REQUIRED_SCORE = 15

class GameBoard:

    def __init__(self, load_game:bool = True, initial_stone_placements:dict = initial_stones_placement):

        self._board_playground = []

        self._prison = {"white": EndlessStack(-1, []), "black": EndlessStack(-1, [])}
            
        self.PreparePlayGround(initial_stone_placements)

        self._history = {}
        self._round = 0

        self._dice_bag = DiceBag()

        self._finish =  {"white": EndlessStack(24, []), "black": EndlessStack(24, [])}

        self._thrown_already = False 
        self._possible_moves = []

        self._all_possible_moves = {}

        self.SetRules("white")

        self.__GenerateAllPossibleMoves()

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


    def AllInHome(self):                    #check
        #area = range(6,24) if player == "white" else range(0,18)
        #return self.CheckOutsideArea(player, area)

        return self.CheckOutsideArea(self._game_rules["home_area"])


    def AllInAcePoint(self):                #check
        #area = range(1,24) if player == "white" else range(0,23)
        #return self.CheckOutsideArea(player, area)

        return self.CheckOutsideArea(self._game_rules["ace_point"])

    def CheckOutsideArea(self,  area):
        outside_area = [point for point in range(0,24) if point not in area]
        #print(outside_area)
        for position in outside_area:
            if self._board_playground[position].CountByColor(self._game_rules["playing"]):
                return False
        return True

    def IsInPrison(self):               #check

        if len(self._prison[self._game_rules["playing"]]) > 0:
            return True
        else:
            return False
        

    
    

    # game update ----------


    def SetRules(self, color):
        if color == "white":
            self._game_rules = {
                "playing" : "white",
                "opponent" : "black",
                "direction" : -1,
                "home_area" : range(0,6),
                "ace_point" : [0],
                "from_prison" : range(18,24),
                "finish_index" : [-1],
                "prison_offset" : 24,
                "score_index": -1,
                "opponent_home" : range(18,24),
            }
            self._round += 1
            self.__WriteHistory(f"{self.GetRound()}. začalo")
        else:
            self._game_rules = {
                "playing" : "black",
                "opponent" : "white",
                "direction" : 1,
                "home_area" : range(18,24),
                "ace_point" : [23],
                "from_prison" : range(0,6),
                "finish_index" : [24],
                "prison_offset" : -1,
                "score_index": 24,
                "opponent_home" : range(0,6),
        }

    def CanScore(self, start_point):
        if not self.AllInHome():    
            #print("not home")       
            return False                           
        for move in self._possible_moves:
            if start_point + (move*self._game_rules["direction"]) == self._game_rules["score_index"]:
                return True


    def GetHomeArea(self):
        return self._game_rules["home_area"]

    def ScoreableIndexes(self):
        a = []
        for point in self._game_rules["home_area"]:
            if self._board_playground[point].CountByColor(self._game_rules["playing"]) > 0:
                for move in self._possible_moves:
                    if point + (move*self._game_rules["direction"]) == self._game_rules["score_index"]:
                        a.append(point)
        return a



    def AvailableMoves(self, start_point):
        if start_point == PRISON:
            return self.GenerateAvailableMoves(start_point)
        
        return self._all_possible_moves[start_point]


    def AskAlreadyThrown(self):
        return self._thrown_already

    def CanContinueTurn(self):
        if self.IsInPrison():
            if len(self.AvailableMoves(PRISON)) == 0:
                return False
        self.__GenerateAllPossibleMoves()
        for key in self._all_possible_moves.keys():
            if len(self._all_possible_moves[key]) > 0:
                return True
            
        return False
    

    def GenerateAvailableMoves(self, start_point):

        if len(self._possible_moves) == 0:
                return []
        
        if start_point == PRISON:
            a = []

            for move in self._possible_moves:
                target = self._game_rules["prison_offset"]+(self._game_rules["direction"]*move)
                if target in self._game_rules["from_prison"]:
                    if self._board_playground[target].CountByColor(self._game_rules["opponent"]) < 2:
                        a.append(target)  
            return a


        available_area = range(0,24)
        unlock_finish = False

        if self._board_playground[start_point].CountByColor(self._game_rules["playing"]) < 1:
            return []

        elif self.AllInHome():
            unlock_finish = True

            if self.AllInAcePoint():
                self._possible_moves = [1 for _ in self._possible_moves]


        available_moves = []

        for move in self._possible_moves:
            target_position = start_point + (move * self._game_rules["direction"])
            if target_position in available_area:
                if self._board_playground[target_position].CountByColor(self._game_rules["opponent"]) < 2:
                    available_moves.append(target_position)
            #if unlock_finish == True:
                #if target_position == self._game_rules["finish_index"]:
                    #...#available_moves.append


        return available_moves


    def Update(self):
        self.__GenerateAllPossibleMoves()

    def EndTurn(self):
        self.__WriteHistory(f"{self._game_rules['playing']} ukončil svůj tah")
        self._thrown_already = False
        self.SetRules(self._game_rules["opponent"])
        self.__WriteHistory(f"{self._game_rules['playing']} je na tahu")
        self._possible_moves = []
        self.__GenerateAllPossibleMoves()



    def GetVictoryType(self):
        if not self.IsVictorious():
            return
        
        if len(self.GetFinish(self._game_rules["opponent"])) > 0:
            return "Basic Victory"
        
        if self.CheckOutsideArea(self._game_rules["opponent_home"]):
            return "BackGammon"

        if len(self.GetFinish(self._game_rules["opponent"])) == 0:
            return "Gammon"



    def __GenerateAllPossibleMoves(self):
        available_area = range(0,24)
        self._all_possible_moves = {}
        for idx in available_area:
            self._all_possible_moves[idx] = self.GenerateAvailableMoves(idx)

    def GetAllPossibleMoves(self):
        return self._all_possible_moves


    def WinCondition(self, player):
        area = range(0,24)

        if not self.IsInPrison(player):
            if self.CheckOutsideArea(player, area):
                pass #he wins


    def __WriteHistory(self, what_to_write:str) -> None:
        if not self.GetRound() in self._history.keys():
            self._history[self.GetRound()] = []
        self._history[self.GetRound()].append(what_to_write)

    def NextRound(self):
        self.PassTurn()

    def PassTurn(self):
        pass

    def MoveStone(self, start_point, target_point):

        if target_point == SCORE_INDEX:
            stone_to_move = self._board_playground[start_point].PopOut()
            self._finish[self._game_rules["playing"]].InsertIn(stone_to_move)
            self.__WriteHistory(f"{self._game_rules['playing']} skoruje s kamenem {stone_to_move.GetIdentity()}, kterým stoupil do finishe")
            self._possible_moves.remove(abs(self._game_rules["score_index"] - start_point))
            #stone_to_move.SaveMovement(target_point)
            self.__GenerateAllPossibleMoves()


        if start_point == PRISON:
            if target_point in self.AvailableMoves(start_point):
                if self._board_playground[target_point].CountByColor(self._game_rules["opponent"]) == 1:
                    self.ToPrison(target_point)
                #print(f"before: {self._possible_moves}")
                stone_to_move = self._prison[self._game_rules["playing"]].PopOut()
                self._board_playground[target_point].InsertIn(stone_to_move)
                self.__WriteHistory(f"{self._game_rules['playing']} utekl z vězení s kamenem {stone_to_move.GetIdentity()} na políčko {self._board_playground[target_point].GetAsChar()}")
                self._possible_moves.remove(abs(self._game_rules["prison_offset"] - target_point))
                #print(f"after: {self._possible_moves}")
                self.__GenerateAllPossibleMoves()

            return      

        if target_point in self._all_possible_moves[start_point]:
            if self._board_playground[target_point].CountByColor(self._game_rules["opponent"]) == 1:
                self.ToPrison(target_point)
            #print(f"before: {self._possible_moves}")
            stone_to_move = self._board_playground[start_point].PopOut()
            self._board_playground[target_point].InsertIn(stone_to_move)
            self.__WriteHistory(f"{self._game_rules['playing']} se posunul s kamenem {stone_to_move.GetIdentity()} na políčko {self._board_playground[target_point].GetAsChar()}")
            self._possible_moves.remove(abs(start_point-target_point))
            #print(f"after: {self._possible_moves}")
            #stone_to_move.SaveMovement(target_point)
            self.__GenerateAllPossibleMoves()


    def ThrowDices(self):
        if self._thrown_already == True:
            return self._possible_moves
        
        dice_throw = self._dice_bag.Throw().copy()

        if dice_throw[0] == dice_throw[1]:
            self._possible_moves = [dice_throw[0] for _ in range(4)]
        else:
            self._possible_moves = list(dice_throw)
        
        self._thrown_already = True
        self.__GenerateAllPossibleMoves()

        self.__WriteHistory(f"{self._game_rules['playing']} ziskal pohyby {self._possible_moves} z hodu kostky")

        return self._possible_moves


    def GetRoundHistory(self, round = 0):
        if round == 0: round = self.GetRound()
        return self._history[round]

    def GetEntireHistory(self):
        return self._history


    def ToPrison(self, target_point):
        stone_to_prison = self._board_playground[target_point].PopOut()
        
        self._prison[self._game_rules["opponent"]].InsertIn(stone_to_prison)
        
        #stone_to_prison.SaveMovement("Prison")

    # Get ----------

    def GetGameSpace(self):
        listing = {}
        for point in self._board_playground:
            listing[point.GetAsInt()] = point.ListStones()
        return listing
    
    def GetStacks(self):
        listing = []
        for idx in range(len(self._board_playground)):
            listing.append(self._board_playground[idx].ListStones())
        return listing


    def GetWhitePrison(self):
        return self._prison["white"].ListStones()
    
    def GetBlackPrison(self):
        return self._prison["black"].ListStones()

    def GetWhiteFinish(self):
        return self._finish["white"].ListStones()
    
    def GetBlackFinish(self):
        return self._finish["black"].ListStones()


    def GetFinish(self, player):
        return self._finish[player]
    

    def GetRound(self):
        return self._round
    
    def GetAvailableMoves(self):
        return self._possible_moves
    
    def GetDices(self):
        if not self._thrown_already:
            return []
        return self._dice_bag.GetState()


    def ListStoneMoveHistory(self, selected_stone):
        all_stacks = self.GetStacks()
        all_stacks.append(self.GetWhiteFinish())
        all_stacks.append(self.GetBlackFinish())
        all_stacks.append(self.GetWhitePrison())
        all_stacks.append(self.GetBlackPrison())
        print(all_stacks)
        

        for stack in all_stacks:
            for stone in stack:
                if stone.GetIdentity() == selected_stone:
                    return stone.GetHistory()
   
        return []

        


    def VictoryPoints(self):
        return len(self._finish[self._game_rules["playing"]])

    def IsVictorious(self):
        if self.VictoryPoints() == REQUIRED_SCORE:
            return 1
        return 0

    #debug ------------

    def PrintGround(self):
        for policko in self._board_playground:
            print(f"{policko.GetAsInt()} - {policko.ListList()}")



def debug():
    gmbrd = GameBoard()

    #gmbrd.PrintGround()

    #gmbrd.MoveStone("white", 5, 7)

    #gmbrd.PrintGround()

    #print("---------------")
    #gmbrd2 = jsonpickle.decode(jsonpickle.encode(gmbrd, unpicklable=True))

    #gmbrd2.PrintGround()

    #print(gmbrd.GetStacks())

    print(gmbrd.ListStoneMoveHistory("white1"))

    #ston = Stone("white", 2, 0)
    #ston.SaveMovement(3)
    #print(ston.GetHistory())
    #
    #zasob = EndlessStack(1, [ston, ston])

if __name__ == "__main__":
    debug()



"""
nacitani a savovani
hrac v nacitani a savovani (ulozit do gameboardu a serializovat)
pravidla inhome, inacepoint
dumpnout vsechno jako slovnik :) /pole
"""