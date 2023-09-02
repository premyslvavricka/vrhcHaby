import PySimpleGUI as gui
import json

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
                [gui.Button("Načíst", key="-LOAD GAME BUTTON-"), gui.Button("Zpět", key="-BACK BUTTON-")]]

        self._game_layout = [
                #[gui.Graph("""gaming board""")], 
                [gui.VSeparator()], 
                [gui.Text("Hraje:", key="-PLAYS BLACK TEXT-"), gui.Text("Player2/AI",key="-BLACK PLAYER-")],
                #[gui.Graph("""player black dices""")],
                [gui.Text("Kolo: xx", key= "-ROUND COUNTER-")], 
                [gui.Text("Hraje:", key="-PLAYS WHITE TEXT-"), gui.Text("Player1",key="-WHITE PLAYER-")], 
                #[gui.Graph("""player white dices""")], 
                [gui.Button("Uložit", key="-SAVE BUTTON-")],
                [gui.Button("Odejít", key="-BACK BUTTON-")]]

        self._window_layout = [
                [gui.Column(self._main_menu_layout, key="-MAIN MENU LAYOUT-", visible=False), 
                 gui.Column(self._load_menu_layout, key="-LOAD MENU LAYOUT-", visible=False),
                 gui.Column(self._game_layout, key="-GAME LAYOUT-", visible=False),]]


        self._window = gui.Window("Backgammon", [[self._window_layout]], size=self._window_size, finalize=True)

    def ShowMainMenu(self):
        self.HideAll()
        self._window["-MAIN MENU LAYOUT-"].update(visible=True)

    def ShowLoadMenu(self):
        self.HideAll()
        self._window["-LOAD MENU LAYOUT-"].update(visible=True)

    def ShowGame(self, ):# one more paramater
        self.HideAll()
        self._window["-GAME LAYOUT-"].update(visible=True)

    def HideAll(self):
        self._window["-MAIN MENU LAYOUT-"].update(visible=False)
        self._window["-LOAD MENU LAYOUT-"].update(visible=False)
        self._window["-GAME LAYOUT-"].update(visible=False)


    def LoadFile(path:str = ""):
        if path[-5:] != ".json":
            gui.popup("Soubor není JSON formátu")
            return
        
        try: #----------------------------------------------------not work yet
            json_file = json.load(open(path))
        except:
            gui.popup("Soubor se nepodařilo otevřít.")



    def Run(self):
        while(True):
            event, values = self._window.read()

            if event in (gui.WINDOW_CLOSED,"-CLOSE BUTTON-"):
                break

            if event == "-LOAD MENU BUTTON-":
                self.ShowLoadMenu()

            if event == "-BACK BUTTON-":
                self.ShowMainMenu()

            if event == "-NEW GAME BUTTON-":
                self.ShowGame()

            if event == "-LOAD GAME BUTTON-":
                self.LoadFile(values["-FILE SEARCH INPUT-"])
                self.ShowGame()




    def Close(self):
        self._window.close()        
