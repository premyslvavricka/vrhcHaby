import window

def main():
    print("start")

    okno = window.GameWindow()
    okno.ShowMainMenu()
    okno.Run()
    okno.Close()

if __name__ == "__main__":
    main()


"""
otevřít okno s hlavním menu
HLAVNI MENU:
    3 tlačítka:
        Nová hra, Načíst, Ukončit

    NOVA HRA:
        --- nova hra bez parametru ---

    NACIST:
        změna hlavního menu na načítací menu
        NACITACI MENU:
            textové pole:
                textové pole pro hledání json souboru se hrou
            2 tlačítka:
                Načíst hru, Zpět

            NACIST HRU:
                --- nacteni hry s parametry ---

            ZPET:
                změna načítací menu na hlavní menu
    
    UKONCIT:
        ukončí hlavní menu

"""