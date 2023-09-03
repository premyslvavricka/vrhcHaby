import PySimpleGUI as gui
import gameboard

class GameWindow:

    def __init__(self, width:int = 800, height:int = 600):
        self._window_size = (width,height)

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

        self._game_layout = [
                #[gui.Graph("""gaming board""")], 
                [gui.VSeparator()], 
                [gui.Text("Hraje:", key="-PLAYS BLACK TEXT-"), gui.Text("Player2/AI",key="-BLACK PLAYER-")],
                #[gui.Graph("""player black dices""")],
                [gui.Text("Kolo: xx", key= "-ROUND COUNTER-")], 
                [gui.Text("Hraje:", key="-PLAYS WHITE TEXT-"), gui.Text("Player1",key="-WHITE PLAYER-")], 
                #[gui.Graph("""player white dices""")], 
                [gui.Button("Uložit", key="-SAVE BUTTON-")],
                [gui.Button("Odejít", key="-BACK BUTTON2-")]]

        self._window_layout = [
                [gui.Column(self._main_menu_layout, key="-MAIN MENU LAYOUT-", visible=False), 
                 gui.Column(self._load_menu_layout, key="-LOAD MENU LAYOUT-", visible=False),
                 gui.Column(self._opponent_select_layout, key="-OPPONENT SELECT LAYOUT-", visible=False),
                 gui.Column(self._game_layout, key="-GAME LAYOUT-", visible=False),]]


        self._window = gui.Window("Backgammon", [[self._window_layout]], size=self._window_size, finalize=True)



    def ShowMainMenu(self):
        self.HideAll()
        self._window["-MAIN MENU LAYOUT-"].update(visible=True)

    def ShowLoadMenu(self):
        self.HideAll()
        self._window["-LOAD MENU LAYOUT-"].update(visible=True)

    def ShowGame(self, gameboard):# one more paramater
        self.HideAll()
        self._window["-GAME LAYOUT-"].update(visible=True)

    def ShowOpponentSelect(self):
        self.HideAll()
        self._window["-OPPONENT SELECT LAYOUT-"].update(visible=True)


    def HideAll(self):
        self._window["-MAIN MENU LAYOUT-"].update(visible=False)
        self._window["-LOAD MENU LAYOUT-"].update(visible=False)
        self._window["-GAME LAYOUT-"].update(visible=False)
        self._window["-OPPONENT SELECT LAYOUT-"].update(visible=False)



    def LoadFile(path:str = ""):
        if path[-5:] != ".json":
            gui.popup("Soubor není JSON formátu")
            return
        
        try: #----------------------------------------------------not work yet
            with open(path, "r") as reader:
                json_file = reader.read()
        except:
            gui.popup("Soubor se nepodařilo otevřít.")


    def Run(self):
        while(True):
            event, values = self._window.read()

            if event in (gui.WINDOW_CLOSED,"-CLOSE BUTTON-"):
                break

            if event == "-LOAD MENU BUTTON-":
                self.ShowLoadMenu()

            if event in [f"-BACK BUTTON{idx}-" for idx in range(3)]:
                self.ShowMainMenu()

            if event == "-NEW GAME BUTTON-":
                self.ShowOpponentSelect()

            if event == "-PLAYER GAME BUTTON-":
                self.ShowGame(gameboard.GameBoard())

            if event == "-AI GAME BUTTON-":
                self.ShowGame(gameboard.GameBoard())

            if event == "-LOAD GAME BUTTON-":
                gui.popup(len(values["-FILE SEARCH INPUT-"]))
                a = self.LoadFile(values["-FILE SEARCH INPUT-"])
                self.ShowGame(gameboard.LoadGame(a))




    def Close(self):
        self._window.close()        
