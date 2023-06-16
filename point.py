import PySimpleGUI as sg
import json


dat = 0
with open("points.json", "r") as F:
    dat = json.load(F)


factions = []
for faction in dat:
    factions.append(faction)

sg.theme('DarkAmber')    # Keep things interesting for your users

# Initial window
layout = [[sg.Text('Points Calculator',key="TITLE_TEXT")],      
          [sg.DropDown(values=factions, size=(20, 12), key='FACTION', readonly=True)],
          [sg.Button('Load Faction'), sg.Exit()]]      
window = sg.Window('40K Points', layout)      
HEIGHT=1
FACTION = ""
while True:                             # The Event Loop
    event, values = window.read() 
    print(event, values)
    
    if event == 'Load Faction':
        factionLayout = [[sg.Text('Points Calculator',key="TITLE_TEXT")],      
          [sg.DropDown(values=factions, size=(20, 12), key='FACTION', readonly=True)],
          [sg.Button('Load Faction'), sg.Exit()],
          [sg.Text("Total: 0", key="FACTION_TOTAL")]
         ]        
        FACTION = values["FACTION"]
        for unit in dat[values["FACTION"]]:
            # Create model count array
            if 'count' not in dat[values["FACTION"]][unit]:
                dat[values["FACTION"]][unit]['count'] = 0   
            
            # create a row 
            row = [sg.Text(unit + " x" + str(dat[values["FACTION"]][unit]['models']), size=(20, HEIGHT)),
                   sg.Text(str(dat[values["FACTION"]][unit]['points']),size=(10, HEIGHT) ),
                   sg.Button('-',size=(2, 1),key=unit+"-"),
                   sg.Button('+',size=(2, 1),key=unit+"+"),
                   sg.Text('x' + str(dat[values["FACTION"]][unit]['models'] * dat[values["FACTION"]][unit]['count']) + ' = ' + str(dat[values["FACTION"]][unit]['points'] * dat[values["FACTION"]][unit]['count']),size=(20, HEIGHT), key=unit+str("TOTAL"))]
            factionLayout.append(row)

        
        window.close()
        window = sg.Window('Window that stays open', factionLayout)      
    elif event == sg.WIN_CLOSED or event == 'Exit':
        break      

    else:
        if event[len(event)-1] == "+":
            dat[FACTION][event[0:len(event)-1]]['count'] += 1
        elif event[len(event)-1] == "-":
            dat[FACTION][event[0:len(event)-1]]['count'] -= 1
            if dat[FACTION][event[0:len(event)-1]]['count'] < 0:
                dat[FACTION][event[0:len(event)-1]]['count'] = 0

        window[event[0:len(event)-1]+str("TOTAL")].update(
'x' + str(dat[FACTION][event[0:len(event)-1]]['models'] * dat[FACTION][event[0:len(event)-1]]['count']) + ' = ' + str(dat[FACTION][event[0:len(event)-1]]['points'] * dat[FACTION][event[0:len(event)-1]]['count'])
)
        FACTION_TOTAL=0
        for unit in dat[FACTION]:
            FACTION_TOTAL += dat[FACTION][unit]['count'] * dat[FACTION][unit]['points']
        window["FACTION_TOTAL"].update("Total: " + str(FACTION_TOTAL))


window.close()
