import PySimpleGUI as gui
import gameboard
import players
import jsonpickle
from datetime import datetime
import math

GAMEBOARD_SIZE = (620, 480)

CANVAS_TRIANGLE_WIDTH = 40
CANVAS_TRIANGLE_HEIGHT = 200

CANVAS_RECTANGLE_AREA_WIDTH = 240
CANVAS_RECTANGLE_AREA_HEIGHT = 200

CANVAS_SPACE_BETWEEN_AREAS_X = 20

CANVAS_OUTER_RECTANGLE_WIDTH = 40
CANVAS_OUTER_RECTANGLE_HEIGHT = 200

CANVAS_INNER_MARGIN_AREAS_Y = 20

CANVAS_OUTER_MARGIN_X = 10
CANVAS_OUTER_MARGIN_Y = 30


class GameWindow:

    def __init__(self, width:int = 800, height:int = 520):
        self._window_size = (width,height) 

        self._hint_points = []

        self._select_first = -10

        self._main_menu_layout = [
                [gui.Text("BackGammon")], 
                [gui.Button("Nová Hra", key="-NEW GAME BUTTON-")], 
                [gui.Button("Načíst Hru", key="-LOAD MENU BUTTON-")], 
                [gui.Button("Ukončit", key="-CLOSE BUTTON-")]]

        self._load_menu_layout = [
                [gui.InputText(key="-FILE SEARCH INPUT-"), gui.FilesBrowse("Hledat", file_types = [("JSON", "*.json")], initial_folder=r"C:\Users\Kuzma\OneDrive\Documents\GitHub\vrhcHaby\Uložené hry")], 
                [gui.Button("Načíst", key="-LOAD GAME BUTTON-"), gui.Button("Zpět", key="-BACK BUTTON0-")]]

        self._opponent_select_layout = [
            [gui.Text("Vyber typ hry:")], 
            [gui.Button("Hráč proti Hráči", key="-PLAYER GAME BUTTON-")], 
            [gui.Button("Hráč prti AI", key="-AI GAME BUTTON-")],
            [gui.Button("Zpět", key="-BACK BUTTON1-")]]

        #self._game_column_board = [[gui.Canvas(size=GAMEBOARD_SIZE, key="-GAMEBOARD-", background_color="white", )]]

        self._game_column_board = [[gui.Graph(GAMEBOARD_SIZE, (0, GAMEBOARD_SIZE[1]), (GAMEBOARD_SIZE[0],0), background_color="brown", enable_events=True, key="-GAMEBOARD-")]]

        self._game_column_players = [
            #[gui.Button("Historie", key="-HISTORY BUTTON-")],
            #[gui.HorizontalSeparator()],
            #[gui.Text("Hraje:", key="-PLAYS BLACK TEXT-", visible=False), 
            # gui.Text("Player2/AI",key="-BLACK PLAYER-")],
            #[gui.Canvas(size=(100, 100), key="-BLACK PLAYER DICES-", background_color="white")],
            #[gui.Button("Hoď kostkami", key="-BLACK THROW BUTTON-", disabled=True), gui.Button("Ukončit tah", key="-END BLACK TURN-", visible=False, disabled=True)],
            [gui.Text("Historie")],
            [gui.Text("", key="-HISTORY TEXT-")],
            [gui.HorizontalSeparator()],
            [gui.Text("Kolo: "), gui.Text("0", key= "-ROUND COUNTER-")], 
            [gui.HorizontalSeparator()],
            [gui.Text("Hraje:"), gui.Text("Player1",key="-PLAYING PLAYER-")], 
            #[gui.Canvas(size=(100, 100), key="-PLAYER DICES-", background_color= "white")],
            [gui.Text("Kostky: "), gui.Text("", key="-LIST DICES-")],
            [gui.Text("Pohyby: "), gui.Text("", key="-POSSIBLE MOVES-")],
            [gui.Button("Hoď kostkami", key="-THROW BUTTON-", disabled=True), 
             gui.Button("Ukončit tah", key="-END TURN BUTTON-", visible=False, disabled=True)],
            [gui.HorizontalSeparator()],
            [gui.Button("Uložit", key="-SAVE BUTTON-"), gui.Button("Odejít", key="-BACK BUTTON2-")]]

        self._game_layout = [[gui.Column(self._game_column_board), 
                              gui.VerticalSeparator(),
                              gui.Column(self._game_column_players)]] 

        self._winner_layout = [[gui.Text("Konec hry")],
                               [gui.Text("", key="-VICTOR TEXT-"), gui.Text("", key="-SCORE TEXT-")],
                               [gui.Button("Domů", key="-HOME BUTTON-")]]                

        self._window_layout = [
                [gui.Column(self._main_menu_layout, key="-MAIN MENU LAYOUT-", visible=False), 
                 gui.Column(self._load_menu_layout, key="-LOAD MENU LAYOUT-", visible=False),
                 gui.Column(self._opponent_select_layout, key="-OPPONENT SELECT LAYOUT-", visible=False),
                 gui.Column(self._game_layout, key="-GAME LAYOUT-", visible=False),
                 gui.Column(self._winner_layout, key="-ENDGAME LAYOUT-", visible=False)]]


        self._window = gui.Window("Backgammon", [[self._window_layout]], size=self._window_size, finalize=True)



    def ShowMainMenu(self):
        self.HideAll()
        self._window["-MAIN MENU LAYOUT-"].update(visible=True)

    def ShowLoadMenu(self):
        self.HideAll()
        self._window["-LOAD MENU LAYOUT-"].update(visible=True)

    def ShowGame(self, gameboard_to_show):# one more paramater
        self.HideAll()
        self._gameboard = gameboard_to_show
        self._window["-GAME LAYOUT-"].update(visible=True)
        self._gameboard.Update()
        self.DrawTriangles()
        self.DrawRectangles()
        self.DrawStones()

        self.UpdateGame()

        self.StartTurn()
        if self._gameboard.AskAlreadyThrown():
            self.InMiddleOfTurn()
        if self._gameboard.AskAlreadyThrown() and (not self._gameboard.CanContinueTurn()):
            self.FinalizeTurn()
    

    def DrawHint(self, selected_idx):

        self.DeleteHints()

        hints = self._gameboard.AvailableMoves(selected_idx)
        #print(f"hints: {hints}")
        for target_position in hints :
            if target_position < 12: 
                self._hint_points.append(self._window["-GAMEBOARD-"].draw_point((self._rectangle_middle_points[target_position][0], self._rectangle_middle_points[target_position][1]-180),10, color="green"))
            else:
                self._hint_points.append(self._window["-GAMEBOARD-"].draw_point((self._rectangle_middle_points[target_position][0], self._rectangle_middle_points[target_position][1]+180),10, color="green"))
        if self._gameboard.CanScore(selected_idx):
            self._hint_points.append(self._window["-GAMEBOARD-"].draw_point((580,240),20, color="green"))

        if len(self._hint_points) != 0:
            self._select_first = selected_idx

        self.UpdateGame()


    def DeleteHints(self):
        for hint_point in self._hint_points:
            self._window["-GAMEBOARD-"].delete_figure(hint_point)
        self._hint_points = []
        self._select_first = -10

    def DrawStones(self):
        self._stone_list = {}
        for stack in self._gameboard.GetStacks():
            for stone in stack:
                self._stone_list[stone.GetIdentity()] = self._window["-GAMEBOARD-"].draw_circle((0,0), 18, fill_color=stone.GetColor())
        for stone in self._gameboard.GetWhitePrison():
            self._stone_list[stone.GetIdentity()] = self._window["-GAMEBOARD-"].draw_circle((0,0), 18, fill_color=stone.GetColor())

        for stone in self._gameboard.GetBlackPrison():
            self._stone_list[stone.GetIdentity()] = self._window["-GAMEBOARD-"].draw_circle((0,0), 18, fill_color=stone.GetColor())

        for stone in self._gameboard.GetWhiteFinish():
            self._stone_list[stone.GetIdentity()] = self._window["-GAMEBOARD-"].draw_circle((0,0), 18, fill_color=stone.GetColor())

        for stone in self._gameboard.GetBlackFinish():
            self._stone_list[stone.GetIdentity()] = self._window["-GAMEBOARD-"].draw_circle((0,0), 18, fill_color=stone.GetColor())


    def MoveStone(self, start_postion, target_position):
        self._gameboard.MoveStone(start_postion, target_position)
        self.DeleteHints()
        self.UpdateActionButton()
        if self._gameboard.IsInPrison():
            self.DrawHint(gameboard.PRISON)
        self.UpdateGame()
    
    def InMiddleOfTurn(self):
        self._window["-THROW BUTTON-"].update(disabled=True)

    def FinalizeTurn(self):
        self._window["-THROW BUTTON-"].update(disabled=True, visible=False)
        self._window["-END TURN BUTTON-"].update(disabled=False, visible=True)

    def StartTurn(self):
        self._window["-PLAYING PLAYER-"].update(self._player_actual.GetName())
        self._window["-END TURN BUTTON-"].update(disabled=True, visible=False)        
        self._window["-THROW BUTTON-"].update(disabled=False, visible=True)
        
    def EndTurn(self):
        self._player_actual, self._player_on_bench = self._player_on_bench, self._player_actual
        self._gameboard.EndTurn()
        self.UpdateGame()

    def DrawTriangles(self):
        origin = [560,450]

        self._rectangle_areas_list = []

        self._rectangle_middle_points = []

        self._triangles = []

        for idx in range(6):
            self._triangles.append(self._window["-GAMEBOARD-"].draw_polygon(
                [(origin[0]-(CANVAS_TRIANGLE_WIDTH*idx), origin[1]), (origin[0]-(CANVAS_TRIANGLE_WIDTH*(idx+1)), origin[1]), (origin[0]-(CANVAS_TRIANGLE_WIDTH/2+CANVAS_TRIANGLE_WIDTH*idx), origin[1]-CANVAS_TRIANGLE_HEIGHT)], fill_color="red"))

            self._rectangle_areas_list.append([(origin[0]-CANVAS_TRIANGLE_WIDTH*idx, origin[1]), (origin[0]-CANVAS_TRIANGLE_WIDTH*(idx+1), origin[1]-CANVAS_TRIANGLE_HEIGHT)])

            self._rectangle_middle_points.append((origin[0]-(CANVAS_TRIANGLE_WIDTH*idx)-(CANVAS_TRIANGLE_WIDTH/2), origin[1]-20))

        origin[0] -= (CANVAS_SPACE_BETWEEN_AREAS_X + CANVAS_RECTANGLE_AREA_WIDTH)

        for idx in range(6):
            self._triangles.append(self._window["-GAMEBOARD-"].draw_polygon(
                [(origin[0]-(CANVAS_TRIANGLE_WIDTH*idx), origin[1]), (origin[0]-(CANVAS_TRIANGLE_WIDTH*(idx+1)), origin[1]), (origin[0]-(CANVAS_TRIANGLE_WIDTH/2+CANVAS_TRIANGLE_WIDTH*idx), origin[1]-CANVAS_TRIANGLE_HEIGHT)], fill_color="red"))

            self._rectangle_areas_list.append([(origin[0]-CANVAS_TRIANGLE_WIDTH*idx, origin[1]), (origin[0]-CANVAS_TRIANGLE_WIDTH*(idx+1), origin[1]-CANVAS_TRIANGLE_HEIGHT)])

            self._rectangle_middle_points.append((origin[0]-(CANVAS_TRIANGLE_WIDTH*idx)-(CANVAS_TRIANGLE_WIDTH/2), origin[1]-20))
        
        origin = [60,30]

        for idx in range(6):
            self._triangles.append(self._window["-GAMEBOARD-"].draw_polygon(
                [(origin[0]+(CANVAS_TRIANGLE_WIDTH*idx), origin[1]), (origin[0]+(CANVAS_TRIANGLE_WIDTH*(idx+1)), origin[1]), (origin[0]+(CANVAS_TRIANGLE_WIDTH/2+CANVAS_TRIANGLE_WIDTH*idx), origin[1]+CANVAS_TRIANGLE_HEIGHT)], fill_color="red"))
            
            self._rectangle_areas_list.append([(origin[0]+CANVAS_TRIANGLE_WIDTH*(idx+1), origin[1]+CANVAS_TRIANGLE_HEIGHT), (origin[0]+CANVAS_TRIANGLE_WIDTH*idx, origin[1])])

            self._rectangle_middle_points.append((origin[0]+(CANVAS_TRIANGLE_WIDTH*idx)+(CANVAS_TRIANGLE_WIDTH/2), origin[1]+20))


        origin[0] += CANVAS_RECTANGLE_AREA_WIDTH + CANVAS_SPACE_BETWEEN_AREAS_X

        for idx in range(6):
            self._triangles.append(self._window["-GAMEBOARD-"].draw_polygon(
                [(origin[0]+(CANVAS_TRIANGLE_WIDTH*idx), origin[1]), (origin[0]+(CANVAS_TRIANGLE_WIDTH*(idx+1)), origin[1]), (origin[0]+(CANVAS_TRIANGLE_WIDTH/2+CANVAS_TRIANGLE_WIDTH*idx), origin[1]+CANVAS_TRIANGLE_HEIGHT)], fill_color="red"))
            
            self._rectangle_areas_list.append([(origin[0]+CANVAS_TRIANGLE_WIDTH*(idx+1), origin[1]+CANVAS_TRIANGLE_HEIGHT), (origin[0]+CANVAS_TRIANGLE_WIDTH*idx, origin[1])]) 

            self._rectangle_middle_points.append((origin[0]+(CANVAS_TRIANGLE_WIDTH*idx)+(CANVAS_TRIANGLE_WIDTH/2), origin[1]+20))

        #print(self._rectangle_middle_points)

    def DrawRectangles(self):

        self._window["-GAMEBOARD-"].draw_rectangle((10, 30), (50, 230), fill_color="red")
        self._window["-GAMEBOARD-"].draw_rectangle((10, 250), (50, 450), fill_color="red")

        self._window["-GAMEBOARD-"].draw_rectangle((570, 30), (610, 230), fill_color="red")
        self._window["-GAMEBOARD-"].draw_rectangle((570, 250), (610, 450), fill_color="red")



    def ClickOnGraph(self, click_position):
        for idx in range(len(self._rectangle_areas_list)):
            if self.InRectangle(click_position, self._rectangle_areas_list[idx]):
                return idx
        return -1 

    def InRectangle(self, click_postion, rectangle):
        if rectangle[0][0] > click_postion[0] > rectangle[1][0]:
            if rectangle[0][1] > click_postion[1] > rectangle[1][1]:
                return True
        return False

    def ShowOpponentSelect(self):
        self.HideAll()
        self._window["-OPPONENT SELECT LAYOUT-"].update(visible=True)


    def HideAll(self):
        self._window["-MAIN MENU LAYOUT-"].update(visible=False)
        self._window["-LOAD MENU LAYOUT-"].update(visible=False)
        self._window["-GAME LAYOUT-"].update(visible=False)
        self._window["-OPPONENT SELECT LAYOUT-"].update(visible=False)
        self._window["-ENDGAME LAYOUT-"].update(visible=False)


    def UpdateGame(self):           #--------------------------- work here
        stacks = self._gameboard.GetStacks()
        for outer_idx in range(len(stacks)):
            stone_distance = CANVAS_TRIANGLE_HEIGHT / max(len(stacks[outer_idx]),1)
            stone_distance = min(40, stone_distance)
            if outer_idx < 12:
                stone_distance = -stone_distance
            for inner_idx in range(len(stacks[outer_idx])):
                #print(f"{outer_idx} : {inner_idx}")
                self._window["-GAMEBOARD-"].relocate_figure(self._stone_list[stacks[outer_idx][inner_idx].GetIdentity()], self._rectangle_middle_points[outer_idx][0]-18, self._rectangle_middle_points[outer_idx][1]+(stone_distance*inner_idx)-18)

        stones_in_prison = self._gameboard.GetWhitePrison()
        print(len(stones_in_prison))
        for idx in range(len(stones_in_prison)):
            self._window["-GAMEBOARD-"].relocate_figure(self._stone_list[stones_in_prison[idx].GetIdentity()], 30-18, 430-18-(idx*20))
            

        stones_in_prison2 = self._gameboard.GetBlackPrison()
        print(len(stones_in_prison2))
        for idx in range(len(stones_in_prison2)):
            self._window["-GAMEBOARD-"].relocate_figure(self._stone_list[stones_in_prison2[idx].GetIdentity()], 30-18, 50-18+(idx*20))

        stones_in_finish = self._gameboard.GetWhiteFinish()
        print(len(stones_in_finish))
        for idx in range(len(stones_in_finish)):
            self._window["-GAMEBOARD-"].relocate_figure(self._stone_list[stones_in_finish[idx].GetIdentity()], 590-18, 430-18-(idx*20))
            

        stones_in_finish = self._gameboard.GetBlackFinish()
        print(len(stones_in_finish))
        for idx in range(len(stones_in_finish)):
            self._window["-GAMEBOARD-"].relocate_figure(self._stone_list[stones_in_finish[idx].GetIdentity()], 590-18, 50-18+(idx*20))   

        self._window["-GAMEBOARD-"].update()

        self._window["-LIST DICES-"].update(str(self._gameboard.GetDices()))
        self._window["-POSSIBLE MOVES-"].update(str(self._gameboard.GetAvailableMoves()))
        self._window["-ROUND COUNTER-"].update(str(int(math.floor(self._gameboard.GetRound()))))





    def LoadFile(self, path_to_file):
        if path_to_file[-5:] != ".json":
            gui.popup("Soubor není JSON formátu")
            return
        
        try: #---------------------------------------------------- maybe work
            with open(path_to_file, "r") as reader:
                json_file = reader.read()
        except:
            gui.popup("Soubor se nepodařilo otevřít.")

        self.DecodeFile(json_file)


    def DecodeFile(self, json_text):
        data = jsonpickle.decode(json_text)

        players.LoadPlayer(data[0])
        players.LoadPlayer(data[1])
        
        gameboard.LoadGame(data[2])


    def SaveGame(self):
        data = []
        data.append(self._player_actual)    
        data.append(self._player_on_bench)
        
        data.append(self._gameboard)

        with open (f"Uložené Hry\\SavedGame{datetime.strftime(datetime.now(),'%Y-%m-%d %H-%M-%S')}.json", "w") as write_file:
            write_file.write(jsonpickle.encode(data))

    def LoadGame(self, path_to_file):
        if path_to_file[-5:] != ".json":
            gui.popup("Soubor není JSON formátu")
            return
        
        try: #---------------------------------------------------- maybe work
            with open(path_to_file, "r") as reader:
                json_file = reader.read()
        except:
            gui.popup("Soubor se nepodařilo otevřít.")        
        a = jsonpickle.decode(json_file)
        self._player_actual = a[0]
        self._player_on_bench = a[1]
        return a[2]



    def UpdateRoundCounter(self):
        pass

    
    def UpdateActionButton(self):
        self._window["-THROW BUTTON-"].update(disabled=True)
        if not self._gameboard.CanContinueTurn():
            self.FinalizeTurn()

    def Run(self):
        while(True):
            event, values = self._window.read()

            if event in (gui.WINDOW_CLOSED,"-CLOSE BUTTON-"):
                break

            if event == "-GAMEBOARD-":

                if (selected_idx := self.ClickOnGraph(values["-GAMEBOARD-"])) != -1:
                    if self._select_first == -10:
                        if not self._gameboard.IsInPrison():
                            self.DrawHint(selected_idx)
                    else:
                        self.MoveStone(self._select_first, selected_idx)
                else:
                    #print(values["-GAMEBOARD-"][0])

                    if self._select_first >= 0:
                        if self._gameboard.CanScore(self._select_first):
                            if 570 < values["-GAMEBOARD-"][0] < 610: 
                                self.MoveStone(self._select_first, gameboard.SCORE_INDEX)
                                if self._gameboard.IsVictorious() == 1:
                                    self._window["-GAMEBOARD-"].erase()
                                    self._window["-GAME LAYOUT-"].update(visible=False)
                                    self._window["-ENDGAME LAYOUT-"].update(visible=True)
                                    self._window["-VICTOR TEXT-"].update(self._player_actual.GetName())
                                    self._window["-SCORE TEXT-"].update(self._gameboard.VictoryPoints())
                        else:
                            self.DeleteHints()

            if event == "-LOAD MENU BUTTON-":
                self.ShowLoadMenu()

            if event in [f"-BACK BUTTON{idx}-" for idx in range(3)]:
                self._window["-GAMEBOARD-"].erase()
                self.ShowMainMenu()

            if event == "-NEW GAME BUTTON-":
                self.ShowOpponentSelect()

            if event == "-PLAYER GAME BUTTON-":
                self._player_actual = players.LocalPlayer("player1", "white")
                self._player_on_bench = players.LocalPlayer("player2", "black")
                self.ShowGame(gameboard.GameBoard())

            if event == "-AI GAME BUTTON-":
                self._player_actual = players.LocalPlayer("player1", "white")
                self._player_on_bench = players.AI("AI", "black")
                self.ShowGame(gameboard.GameBoard())

            if event == "-LOAD GAME BUTTON-":
                #a = self.LoadFile(values["-FILE SEARCH INPUT-"])
                a = self.LoadGame(values["-FILE SEARCH INPUT-"])
                #self.ShowGame(self.LoadFile(a))
                self.ShowGame(a)

            if event == "-SAVE BUTTON-":
                self.SaveGame()

            if event == "-THROW BUTTON-":
                self._gameboard.ThrowDices()
                self._window["-THROW BUTTON-"].update(disabled=True)
                if not self._gameboard.CanContinueTurn():
                    self.FinalizeTurn()
                if self._gameboard.IsInPrison():
                    self.DrawHint(gameboard.PRISON)
                self.UpdateGame()

            if event == "-END TURN BUTTON-":
                self.EndTurn()
                if self._player_actual.GetName() == "AI" and self._player_actual.DoTurn(self._gameboard):
                    if self._gameboard.IsVictorious() == 1:
                        self._window["-GAMEBOARD-"].erase()
                        self._window["-GAME LAYOUT-"].update(visible=False)
                        self._window["-ENDGAME LAYOUT-"].update(visible=True)
                        self._window["-VICTOR TEXT-"].update(self._player_actual.GetName())
                        self._window["-SCORE TEXT-"].update(self._gameboard.VictoryPoints())
                        continue
                    self.EndTurn()

                self.StartTurn()

            if event == "-HOME BUTTON-":
                self.HideAll()
                self.ShowMainMenu()


    def Close(self):
        self._window.close()        
