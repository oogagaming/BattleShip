from random import randint, randrange
import PySimpleGUI as sg

again = False

def BattleShip():
    blank_pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc````\x00\x00\x00\x05\x00\x01\xa5\xf6E@\x00\x00\x00\x00IEND\xaeB`\x82'

    sg.theme('DarkBlue15')
    layout =    [[sg.Text('BattleShip')],
                [sg.B('Restart',key="clear",disabled=False), sg.VerticalSeparator(pad=None),sg.Button('Exit')],
                [sg.Text("",key="win-text")]]

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
    icon = "images\\1461855.ico"

    window = sg.Window('BattleShip Game', layout,resizable=True,size = (550,620),icon=icon)
    clicks = 0
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
        
        if event in ships:
            window[event].update("X",disabled=True,button_color = ('Red','Red'))
            ships = [i for i in ships if i!=event]
            clicks += 1
        elif event != "clear":
            window[event].update("O",disabled=True)
            clicks += 1
        
        if len(ships) == 0:
            winText = "You Sunk All the Ships in "+str(clicks)+" clicks"
            window["win-text"].update(winText,font=("",20))
            for i in cells:
                window[i].update(disabled=True)
    window.close()
BattleShip()
while again:
    BattleShip()