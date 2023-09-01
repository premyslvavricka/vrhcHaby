import PySimpleGUI as gui
import json

class Menu:

    def __init__(self, width = 1280, height = 720):
        self._width = width
        self._height = height
        self._hlavni_layout = [[gui.Text("BackGammon")], [gui.Button("Nová Hra", key="-NEW GAME BUTTON-")], 
                        [gui.Button("Načíst Hru", key="-LOAD MENU BUTTON-")], 
                        [gui.Button("Ukončit", key="-CLOSE BUTTON-")]]
        self._nacist_layout = [[gui.InputText(key="-FILE SEARCH-"), 
                                gui.FilesBrowse("Hledat", file_types = [("JSON", "*.json")], initial_folder=r"C:\Users\Kuzma\OneDrive\Documents\GitHub\vrhcHaby\Uložené hry")], [gui.Button("Načíst", key="-LOAD BUTTON-"), gui.Button("Zpět", key="-BACK BUTTON-")]]
        self._layout = [[gui.Column(self._hlavni_layout, key="-MAIN MENU LAYOUT-"), 
                        gui.Column(self._nacist_layout, key="-LOAD MENU LAYOUT-", visible=False)]]

    def UkazSe(self):
        okno_menu = gui.Window("Backgammon - Menu", self._layout, size=(self._width, self._height))

        while(True):
            event, values = okno_menu.read()

            if event in (gui.WINDOW_CLOSED, "-CLOSE BUTTON-"):
                break

            if event == "-LOAD MENU BUTTON-":
                okno_menu["-MAIN MENU LAYOUT-"].update(visible=False)
                okno_menu["-LOAD MENU LAYOUT-"].update(visible=True)

            if event == "-BACK BUTTON-":
                okno_menu["-LOAD MENU LAYOUT-"].update(visible=False)
                okno_menu["-MAIN MENU LAYOUT-"].update(visible=True)

            if event == "-NEW GAME BUTTON-":
                pass #new window with game

            if event == "-LOAD BUTTON-":
                if values["-FILE SEARCH-"][-5:] == ".json":
                    try: #----------------------------------------------------not work yet
                        json_file = json.load(open(values["-FILE SEARCH-"]))
                    except:
                        gui.popup("Soubor se nepodařilo otevřít.")

        okno_menu.close()


okno_menu = Menu()

okno_menu.UkazSe()