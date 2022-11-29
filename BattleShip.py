from random import randint, randrange
import PySimpleGUI as sg

again = False

icon = "images\\1461855.ico"

def ReadPoints():
    points = []
    with open("LeaderBoard.txt", "r") as outfile:
        for line in outfile:
            line = line.strip("\n")
            points.append(int(line))

    points.sort()
    print(points)
    print(points[0:10])
    return points[0:10]

def WritePoints(score):
    print("wrote points ",score)
    with open("LeaderBoard.txt", "a") as outfile:
        score = str(score) + "\n"
        outfile.writelines(score)
        print(outfile)

def LeaderBoard():
    sg.theme('DarkBlue14')
    layout = [[sg.Button('Exit',pad=(10,30),button_color="Red")]]

    points = ReadPoints()
    points.sort(reverse=True)
    for i in points:
        text = [sg.Text(str(i))]
        layout.insert(0,text)
    
    layout.insert(0,[sg.Text("Top 10 Lowest Scores",font=("",14))])
    
    window = sg.Window('Leaderboard', layout,resizable=True,size = (350,390),icon=icon)

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
                [sg.Text(" ",key="win-text",font=("",20))]]

    width = 12
    height = 12
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

    window = sg.Window('BattleShip Game', layout,resizable=True,size = (550,645),icon=icon)
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