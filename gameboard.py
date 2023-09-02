from random import randint

class EndlessStack:
    """
    Třída slouží k reprezentování kamenů na jednotlivým políčku
    - initial_stones = list, který slouží k naplnění políčka kameny na začátku či načtení hry
    """

    def __init__(self, identity:int, initial_stones:list = []):
        self._identityChr = chr(97 + identity)              #pisemne oznaceni policka
        self._identityInt = identity                        #ciselne oznaceni policka
        self._stones_list = initial_stones                  #seznam s kameny
        self._current_list_size = len(self._stones_list)    #delka seznamu

        self._held_color = str                              #barva kamenu v seznamu
        self.__SetColor()


    def __SetColor(self):           #nastavuje barvu podle kamenu v seznamu
        if self._current_list_size > 0:
            self._held_color = self._stones_list[0].GetColor()
        else:
            self._held_color = "None"

    def InsertIn(self, stone_to_insert):            #vklada kamen do seznamu
        self._stones_list.append(stone_to_insert)
        self._current_list_size += 1
        self.__SetColor()

    def PopOut(self):               #vyhazuje vrchni prvek seznamu
        if self._current_list_size > 0:
            self._current_list_size -= 1
            self.__SetColor()
            return self._stones_list.pop(self._current_list_size)
    
    def GetSelfChr(self):       #vraci pismene oznaceni policka
        return self._identityChr
    
    def GetSelfInt(self):       #vraci ciselne oznaceni policka
        return self._identityInt
    
    def GetHeldColor(self):
        return self._held_color

    def ListList(self):
        return [self._stones_list[idx].GetSelf() for idx in range(self._current_list_size)]


class DiceBag:
    """
    Třída slouží k vygenerování náhodného hodu dvou kostky do hry
    """

    def __init__(self):
        self._dices_throw = tuple

    def Throw(self):
        self._dices_throw = (randint(1,6), randint(1,6))
        return self._dices_throw

    def GetState(self):
        return self._dices_throw
    

class Stone():

    def __init__(self, color:str, number:int):
        self._color = color
        self._identity = color[0] + str(number)

    def GetColor(self):
        return self._color

    def GetSelf(self):
        return self._identity



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

initial_stones_placement = {0:[Stone("black", 0), Stone("black", 1)], 
                            1:[], 2:[], 3:[], 4:[], 
                            5:[Stone("white", 0), Stone("white", 1), Stone("white", 2), Stone("white", 3), Stone("white", 4)], 
                            6:[],
                            7:[Stone("white", 5), Stone("white", 6), Stone("white", 7)],
                            8:[], 9:[], 10:[],
                            11:[Stone("black", 2), Stone("black", 3), Stone("black", 4), Stone("black", 5), Stone("black", 6)],
                            12:[Stone("white", 8), Stone("white", 9), Stone("white", 10), Stone("white", 11), Stone("white", 12)],
                            13:[], 14:[], 15:[],
                            16:[Stone("black", 7), Stone("black", 8), Stone("black", 9)],
                            17:[],
                            18:[Stone("black", 10), Stone("black", 11), Stone("black", 12), Stone("black", 13), Stone("black", 14)],
                            19:[], 20:[], 21:[], 22:[],
                            23:[Stone("white", 13), Stone("white", 14)]}


class GameBoard:

    def __init__(self, initial_stone_placements:dict = initial_stones_placement):
        self._board_playground = []
        self.PreparePlayGround(initial_stone_placements)

        self._prison_white = EndlessStack(24)
        self._prison_black = EndlessStack(25)

        self._finish_white = []
        self._finish_black = []

        self._dice_moves = []


    def PreparePlayGround(self, initial_stone_placements:dict):
        for idx in range(24):
            self._board_playground.append(EndlessStack(idx,initial_stone_placements[idx]))

    def IsValid(self, player, policko1, policko2):
        pass

    def AllInHome(self, player):
        if player == "white":
            area = range(6,24)
        else:
            area = range(0, 18)

        print(list(area))

        for idx in area:
            print(f"{player}  {self._board_playground[idx].GetHeldColor()}")
            if player == self._board_playground[idx].GetHeldColor():
                return False
                
        return True


    def PossibleMoves(self, player, policko1):
        pass

    def WinCondition(self):
        pass

    def GetHistory(self):
        pass

    def WriteHistory(self, what_to_write:str):
        pass

    def MoveStone(self, player, policko1, policko2):
        pass

    def ToPrison(self, player, policko):
        pass

    def FromPrison(self, player, policko2):
        pass

    def IsInPrison(self, player):
        pass

    def GetGameSpace(self):
        pass

    def GetPrison(self, player):
        pass

    def GetFinish(self, player):
        pass

    def AllInAcePoint(self, player):
        pass

    def GetDices(self):
        pass

    def PrintGround(self):
        for policko in self._board_playground:
            print(f"{policko.GetSelfInt()} - {policko.ListList()}")

    def fuck(self):
        print(self._board_playground[6].ListList())



gmbrd = GameBoard()

#gmbrd.PrintGround()

print(gmbrd.AllInHome("black"))


zasobnikos = EndlessStack(1,[])

zasobnikos.ListList()