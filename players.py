#třídy: zásobník, kostka?, hrací deska, hráč1 - hráč2, AI, printer
from random import randint

class EndlessStack:
    """
    Třída slouží k reprezentování kamenů na jednotlivým políčku
    - initial_stones = list, který slouží k naplnění políčka kameny na začátku či načtení hry
    """

    def __init__(self, initial_stones:list = []):
        self._stones_list = initial_stones
        self._current_list_size = len(self._stones_list)

    def InsertIn(self, stone_to_insert):
        self._stones_list.append(stone_to_insert)
        self._current_list_size += 1

    def PopOut(self):
        self._current_list_size -= 1
        return self._stones_list.pop(self._current_list_size)
    
    #def ListOne(self, idx:int = 0):
    #    return self._stones_list[idx].GiveSelf()

    def ListList(self):
        return [self._stones_list[idx].GiveSelf() for idx in range(self._current_list_size)]


class Dices:
    """
    Třída slouží k vygenerování náhodného hodu dvou kostky do hry
    """

    def __init__(self):
        self._dices_throw = tuple

    def Throw(self):
        self._dices_throw = (randint(1,6), randint(1,6))

    def Read(self):
        return self._dices_throw
    

class Stone():

    def __init__(self, color:str, number:int):
        self._color = color
        self._identity = color[0] + str(number)

    def GiveColor(self):
        return self._color

    def GiveSelf(self):
        return self._identity




kameny = [Stone("white",idx+1) for idx in range(5)]

zasobnik1 = EndlessStack(kameny)

print(zasobnik1.ListList())

a = zasobnik1.PopOut()

print(a.GiveColor())

print(zasobnik1.ListList())


