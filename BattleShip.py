from random import randint, randrange
import PySimpleGUI as sg

again = False

board = [68,420,69,180]
board.sort(reverse=True)


def ReadPoints():
    points = []
    with open("LeaderBoard.txt", "r") as outfile:
        for line in outfile:
            line = line.strip("\n")
            points.append(int(line))
    print(points)
    return points

def WritePoints(score):
    print("wrote points ",score)
    with open("LeaderBoard.txt", "a") as outfile:
        score = str(score) + "\n"
        outfile.writelines(score)
        print(outfile)

def LeaderBoard():
    sg.theme('DarkBlue15')
    layout = [[sg.Button('Exit')]]

    points = ReadPoints()
    points.sort()
    for i in points:
        text = [sg.Text(str(i))]
        layout.insert(0,text)

    window = sg.Window('Leaderboard', layout,resizable=True,size = (450,620))

    while True:
        event, values = window.read()
        print(event, values)

        if event == "Exit":
            break
    window.close()


def BattleShip():
    blank_pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E@\x00\x00\x00\x00IEND\xaeB`\x82'

    sg.theme('DarkBlue15')
    layout =    [[sg.Text('BattleShip')],
                [sg.B('Restart',key="clear",disabled=False), sg.VerticalSeparator(pad=None),sg.Button('Exit'),sg.VerticalSeparator(pad=None),sg.Button('Leaderboard')],
                [sg.Text("",key="win-text")]]

    width = 8
    height = 8
    cells = []
    #generate all cells
    for i in range(height):
        row = []
        for j in range(width):
            key=(i+1,j+1)
            cells.append(key)
            butt = sg.Button(" ",key=key ,image_data=blank_pixel, font=("", 25, "bold"), image_size=(40, 40),button_color = ('white','dark grey'),pad = (0,0))
            row.append(butt)
        layout.append(row)
    ships = []
    #Generate ships
    avail_ships = [5,4,3,3,2]
    for i in avail_ships:
        x = randint(1,height)
        y = randint(1,width)
        ships.append((x,y))
        if i + x > height:
            for j in range(i-1):
                x -= 1
                ships.append((x,y))
        else:
            for j in range(i-1):
                x += 1
                ships.append((x,y))
    icon = "images\\1461855.ico"

    window = sg.Window('BattleShip Game', layout,resizable=True,size = (550,620),icon=icon)
    clicks = 0
    won = False
    
    while True:
        event, values = window.read()
        # print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            global again
            again = False
            break
        elif event == "clear":
            again = True
            break
        
        if event == "Leaderboard":
            LeaderBoard()

        if event in ships:
            window[event].update("X",disabled=True,button_color = ('Red','Red'))
            ships = [i for i in ships if i!=event]
            clicks += 1
        elif type(event) == tuple:
            window[event].update("O",disabled=True)
            clicks += 1
        
        if len(ships) == 0 and not won:
            won = True
            winText = "You Sunk All the Ships in "+str(clicks)+" clicks"
            window["win-text"].update(winText,font=("",20))
            WritePoints(clicks)
            for i in cells:
                window[i].update(disabled=True)
    window.close()



BattleShip()
while again:
    BattleShip()