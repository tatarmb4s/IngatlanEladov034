#Athor: Copyright © 2023: Tatár Mátyás Bence (https://github.com/tatarmb4s/) - All Right Reserved

# Snake feladat, kibővítve almával és pontszámítással. Egy két debug és extra parancs is került bele.

from random import randint as ri


snakeSize = 1 #kígyó pontok száma / aktuális mérete
snake = [[0,1]] # kígyó helyei, tömbben
almaPos = [0,0] # alma helye

width = 60 # képernyő szélessége
height = 30 # képernyő hossza
screen = [] # képernyő adatai

lastIrany = "le"

# alaphelyzetbe állítja a kijelzőt ráirás előtt
def screenNuller():
    global screen
    screen = []
    for i in range(height):
        for e in range(width):
            symbol=f" "
            if i == 0 or e == 0 or i==height-1 or e == width-1:
                symbol=f"*"
            y = [symbol]
            try:
                screen[i].append(symbol)
            except:
                screen.append(y)
# kiírja a kijelzőre az adatait
def screenFiller():
    for i in range(len(snake)):
        screen[snake[i][1]][snake[i][0]] = "@"
    screen[almaPos[1]][almaPos[0]] = "🍎"
# elhelyezi az almát egy random helyre. Feature, hogy a kígyóra is teheti, teszelhetjük a szerencsénket vele.
def almaPoser():
    global almaPos
    almaPos = [ri(1,width-2),ri(1,height-2)]
# Kiírja a consoleba a képernyő tartalmát
def printScreen():
    for i in range(len(screen)):
        # print("-", end="\n")
        print("", end="\n")
        for e in range(len(screen[i])):
            symbol = screen[i][e][0]
            print(screen[i][e][0], end="", sep="")
    print("")
# Játék végén aktiválódik, amikor vesztettél.
def loose(indok):
    print(("-"*len(f"Vesztettél. {indok}")), f"\nVesztettél. {indok} \n\tPontjaid: {snakeSize}\nMost ennyi volt, szép napot.\n",("-"*len(f"Vesztettél. {indok}")),"\n\n")    
    exit()
# Mozgatja a kígyót a kijelzőn a kígyó méret alapján            
def snakeMover(nextX, nextY):
    global snake
    global snakeSize
    global almaPos
    nextCord = [nextX, nextY]
    isCordin = not [nextX, nextY] in snake
    snake.append(nextCord)
    if nextY< 29 and nextY > 0 and nextX < 59 and nextX > 0 and isCordin:    
        if snake[-1] == almaPos:
            snakeAdder()
            almaPoser()
        if len(snake) > snakeSize:
            snake.pop(0)
        for i in range(len(snake)):
            screen[snake[i][1]][snake[i][0]] = "@"
    else:
        if not isCordin:
            loose("Saját magadnak mentél!")
        else:
            loose("Kimentél a pályáról!")
        
#hozzáadja az alma pontot
def snakeAdder():
    global snakeSize
    snakeSize+=1
# Egy kör a játékban, minen körben clearelődik a konzol az élmény érdekében.
def GameRound():
    global lastIrany
    irany, debug = input("Hova?\n"), ""
    if irany == "":
        irany = lastIrany
    else:
        lastIrany = irany
    if irany=="jobbra" or irany=="jobb":
        nX, nY = snake[-1][0]+1, snake[-1][1]
        snakeMover(nX, nY)
    elif irany=="balra" or irany=="bal":
        nX, nY = snake[-1][0]-1, snake[-1][1]
        snakeMover(nX, nY)
    elif irany=="fel":
        nX, nY = snake[-1][0], snake[-1][1]-1
        snakeMover(nX, nY)
    elif irany=="le":
        nX, nY = snake[-1][0], snake[-1][1]+1
        snakeMover(nX, nY)
    elif irany=="x" or irany=='meguntam':
        print(("-"*len(f"Játék vége. ")), f"\nJáték vége.  \n\tPontjaid: {snakeSize}\nMost ennyi volt, szép napot.\n",("-"*len(f"Játék vége. ")),"\n\n")    
        exit()
    elif irany=="sn":
        debug = snake
    elif irany=="ap":
        debug = almaPos
    print("\033c", end='')
    
    screenNuller(), screenFiller(), printScreen()
    print(debug)
# A játékot indítja el.
def StartGame():
    screenNuller()
    global snake
    snake = [[ri(1,width-2),ri(1,height-2)]]
    almaPoser(), screenFiller(), printScreen()
    while(True):
        GameRound()
StartGame()

#Athor: Copyright © 2023: Tatár Mátyás Bence (https://github.com/tatarmb4s/) - All Right Reserved