import ipaddress
import gooeypie as gp
from configparser import ConfigParser
import os
from os.path import exists
import requests
import ctypes
import webbrowser

if not os.path.exists(os.path.join(os.environ['APPDATA'], 'OpenSesame')):
    os.mkdir(os.path.join(os.environ['APPDATA'], 'OpenSesame'))

# defining very important stuff
CONFIG_FILE_PATH = os.path.join(os.environ['APPDATA'], 'OpenSesame')
CONFIG_FILE = os.path.join(CONFIG_FILE_PATH, 'config.ini')

# create config file if it doesn't exist
if not exists(CONFIG_FILE):
    open(CONFIG_FILE, "x")

# set default values for all global variables until we check config
global controllerIPaddr
controllerIPaddr = '127.0.0.1'
global controllerUser
controllerUser = 'admin'
global controllerPasswd
controllerPasswd = 'admin'
global controllerDuration
controllerDuration = '10'

global doors
doors = 0
global opnDoorID
opnDoorID = ''

global door1Name
door1Name = ''
global door2Name
door2Name = ''
global door3Name
door3Name = ''
global door4Name
door4Name = ''
global door5Name
door5Name = ''
global door6Name
door6Name = ''
global door7Name
door7Name = ''
global door8Name
door8Name = ''
global door9Name
door9Name = ''

global door1ID
door1ID = ''
global door2ID
door2ID = ''
global door3ID
door3ID = ''
global door4ID
door4ID = ''
global door5ID
door5ID = ''
global door6ID
door6ID = ''
global door7ID
door7ID = ''
global door8ID
door8ID = ''
global door9ID
door9ID = ''

global doorsList
doorsList = []

global console_togSwitch
console_togSwitch = False

config = ConfigParser() # defining configparser to config so we can shorthand it for the rest of the script

def raise_console(console_toggle):
    ## props to tgikal on stackoverflow 4 dis 1 ##
    if console_toggle:
        # open console for bugs, errors output
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 4)
    
    else:
        # hide the console
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def validIPcheck(value):
    ## props to elizabeth shipton on abstractapi.com 4 dis 1  ##
    if(value):
        try:
            value = ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

def save_config(title, name, value):
    if not config.has_section(title):
        config.add_section(title)

    config.set(title, name, value)
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def rem_config(title, name):
    if not config.has_option(title, name):
        app.alert('Error: Config doesn\'t have that option.', 'We couldn\t remove that option from the config as it isn\t present.', 'warning')
    
    config.remove_option(title, name)
    
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)
        configfile.close()

def read_config(): # read config and reassign values to variables
    global controllerIPaddr
    global controllerUser
    global controllerPasswd
    global controllerDuration
    global doors
    
    global door1Name
    global door1Name
    global door2Name
    global door3Name
    global door4Name
    global door5Name
    global door6Name
    global door7Name
    global door8Name
    global door9Name
    # make sure we have all our global values here so they aren't local in the function
    global door1ID
    global door1ID
    global door2ID
    global door3ID
    global door4ID
    global door5ID
    global door6ID
    global door7ID
    global door8ID
    global door9ID
    
    global doorsList
    
    config.read(CONFIG_FILE)
    
    for i in range(1,24): # this whole for loop is wizardry, idk how i did it but i did it
        if not config.has_option('DOORS', 'DOOR{dID}'.format(dID=i)): # if there isn't a value in any of the 1-24
            ni = i # check next entry for values
            while not config.has_option('DOORS', 'DOOR{dID}'.format(dID=i)): # while there's not a value for our empty entry
                ni = ni+1 # if there isn't one, keep checking down the last until u find one or max out door amt aka 9 atm
                #print("i = "+str(i))
                #print("ni = "+str(ni))
                
                if(config.has_option('DOORS', 'DOOR{ndID}'.format(ndID=ni))): # IF we find a door entry past the empty entry, take that entry and make it the current empty one and then delete it.
                    rawDvalue = config.get('DOORS', 'DOOR{dID}'.format(dID=ni))
                    save_config('DOORS', 'DOOR{dID}'.format(dID=i), rawDvalue)
                    rem_config('DOORS', 'DOOR{dID}'.format(dID=ni))
                
                if(ni > 24):
                    break
    
    # assign saved values from config file to variables for persistance
    if config.has_option('CONTROLLER', 'cntlripaddr'):
        savedIP = config.get('CONTROLLER', 'cntlripaddr')
        if validIPcheck(savedIP) == True:
            controllerIPaddr = savedIP
    else:
        controllerIPaddr = '127.0.0.1'
    
    print('controllerIPaddr is:{cntrip}'.format(cntrip=controllerIPaddr))

    if config.has_option('CONTROLLER', 'cntlrUser'):
        cntlrUser = config.get('CONTROLLER', 'cntlrUser')
        controllerUser = str(cntlrUser)
        print('controllerUser is:{cntrusr}'.format(cntrusr=controllerUser))
    
    else:
        controllerUser = 'admin'

    if config.has_option('CONTROLLER', 'cntlrPasswd'):
        cntlrPasswd = config.get('CONTROLLER', 'cntlrPasswd')
        controllerPasswd = str(cntlrPasswd)
        print('controllerPasswd is:{cntrpwd}'.format(cntrpwd=controllerPasswd))
    
    else:
        controllerPasswd = 'admin'
    
    if config.has_option('CONTROLLER', 'cntlrDuration'):
        cntlrDuration = config.get('CONTROLLER', 'cntlrDuration')
        controllerDuration = str(cntlrDuration)
        print('controllerDuration is:{cntrdur}'.format(cntrdur=controllerDuration))
    else:
        controllerDuration = '10'

    if config.has_option('DOORS', 'amount'):
        savedDoorAmount = config.get('DOORS', 'amount')
        print('savedDoorAmount is equal to: {rSavedDoor}'.format(rSavedDoor=savedDoorAmount))
        if savedDoorAmount.isnumeric():
            doors = int(savedDoorAmount)
            print('savedDoorAmount is numeric and doors amount has been reassigned from config')
            
        else:
            doors = 0
    print('savedDoorAmount has set doors to:{sda}'.format(sda=doors))

    if config.has_option('DOORS', 'DOOR1'):
        door1Raw = config.get('DOORS', 'DOOR1') # assign a string the saved list (as a string) from our config
        door1RawList = door1Raw.split(",") # converts the raw string from config to a list
        door1Name = door1RawList.pop(0) # assigns the first value in the list to doorName
        door1ID = door1RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door1Name not in doorsList):
            doorsList.append(door1Name) # append to our list of doors for remove menu
        

    if config.has_option('DOORS', 'DOOR2'):
        door2Raw = config.get('DOORS', 'DOOR2') # assign a string the saved list (as a string) from our config
        door2RawList = door2Raw.split(",") # converts the raw string from config to a list
        door2Name = door2RawList.pop(0) # assigns the first value in the list to doorName
        door2ID = door2RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door2Name not in doorsList):
            doorsList.append(door2Name) # append to our list of doors for remove menu
        

    if config.has_option('DOORS', 'DOOR3'):
        door3Raw = config.get('DOORS', 'DOOR3') # assign a string the saved list (as a string) from our config
        door3RawList = door3Raw.split(",") # converts the raw string from config to a list
        door3Name = door3RawList.pop(0) # assigns the first value in the list to doorName
        door3ID = door3RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door3Name not in doorsList):
            doorsList.append(door3Name) # append to our list of doors for remove menu
        
    
    if config.has_option('DOORS', 'DOOR4'):
        door4Raw = config.get('DOORS', 'DOOR4') # assign a string the saved list (as a string) from our config
        door4RawList = door4Raw.split(",") # converts the raw string from config to a list
        door4Name = door4RawList.pop(0) # assigns the first value in the list to doorName
        door4ID = door4RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door4Name not in doorsList):
            doorsList.append(door4Name) # append to our list of doors for remove menu
        
    
    if config.has_option('DOORS', 'DOOR5'):
        door5Raw = config.get('DOORS', 'DOOR5') # assign a string the saved list (as a string) from our config
        door5RawList = door5Raw.split(",") # converts the raw string from config to a list
        door5Name = door5RawList.pop(0) # assigns the first value in the list to doorName
        door5ID = door5RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door5Name not in doorsList):
            doorsList.append(door5Name) # append to our list of doors for remove menu
        
    
    if config.has_option('DOORS', 'DOOR6'):
        door6Raw = config.get('DOORS', 'DOOR6') # assign a string the saved list (as a string) from our config
        door6RawList = door6Raw.split(",") # converts the raw string from config to a list
        door6Name = door6RawList.pop(0) # assigns the first value in the list to doorName
        door6ID = door6RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door6Name not in doorsList):
            doorsList.append(door6Name) # append to our list of doors for remove menu
        
    
    if config.has_option('DOORS', 'DOOR7'):
        door7Raw = config.get('DOORS', 'DOOR7') # assign a string the saved list (as a string) from our config
        door7RawList = door7Raw.split(",") # converts the raw string from config to a list
        door7Name = door7RawList.pop(0) # assigns the first value in the list to doorName
        door7ID = door7RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door7Name not in doorsList):
            doorsList.append(door7Name) # append to our list of doors for remove menu
        
    
    if config.has_option('DOORS', 'DOOR8'):
        door8Raw = config.get('DOORS', 'DOOR8') # assign a string the saved list (as a string) from our config
        door8RawList = door8Raw.split(",") # converts the raw string from config to a list
        door8Name = door8RawList.pop(0) # assigns the first value in the list to doorName
        door8ID = door8RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door8Name not in doorsList):
            doorsList.append(door8Name) # append to our list of doors for remove menu

    if config.has_option('DOORS', 'DOOR9'):
        door9Raw = config.get('DOORS', 'DOOR9') # assign a string the saved list (as a string) from our config
        door9RawList = door9Raw.split(",") # converts the raw string from config to a list
        door9Name = door9RawList.pop(0) # assigns the first value in the list to doorName
        door9ID = door9RawList.pop(-1) # assigns the last value in the list to doorID
        
        if(door9Name not in doorsList):
            doorsList.append(door9Name) # append to our list of doors for remove menu
    
    print('\ndoorsList is equal to:{drlst}'.format(drlst=doorsList))

def whichDoor(event): # choose which door based on widget (button) pressed
    global opnDoorID
    
    if event.widget == door1Button:
        opnDoorID = door1ID
        openDoor()
    if event.widget == door2Button:
        opnDoorID = door2ID
        openDoor()
    if event.widget == door3Button:
        opnDoorID = door3ID
        openDoor()
    if event.widget == door4Button:
        opnDoorID = door4ID
        openDoor()
    if event.widget == door5Button:
        opnDoorID = door5ID
        openDoor()
    if event.widget == door6Button:
        opnDoorID = door6ID
        openDoor()
    if event.widget == door7Button:
        opnDoorID = door7ID
        openDoor()
    if event.widget == door8Button:
        opnDoorID = door8ID
        openDoor()
    if event.widget == door9Button:
        opnDoorID = door9ID
        openDoor()

def openDoor():
    global opnDoorID
    print("\nopening door... {opnDOORID}".format(opnDOORID=opnDoorID))
    
    try:
        reqControllerIP = 'http://' + controllerIPaddr + ':18779/infinias/ia/Doors'
    
        payload = {
        'Username': controllerUser,
        'Password': controllerPasswd,
        'LockStatus': 'Unlocked',
        'Duration': controllerDuration,
        'DoorIds': opnDoorID
        }
        
        print(payload)
        
        r = requests.put(reqControllerIP, payload)
        r.raise_for_status()
        
        print(r)
        print(r.content)
    except requests.exceptions.HTTPError as err:
        print(err)
        app.alert('RESTful API Request Error', 'Pleae review the request in the console output and make sure the credentials and IP address are correct.', 'error')
        print("\nThere was an error in opening your door!\nPleae review the request and make sure the credentials and IP address are correct.")
        raise_console(True)
    

def open_controllerSetup(event):
    controllerSetup.show_on_top()

def controllerSetupSave(event):
    global controllerIPaddr
    global controllerUser
    global controllerPasswd
    global controllerDuration
    
    # ip address
    if(controllerIP_inp.text) and validIPcheck(controllerIP_inp.text) == True:
        save_config('CONTROLLER', 'cntlripaddr', controllerIP_inp.text)
        
        # update the GUI text and variables
        controllerIPaddr = controllerIP_inp.text
        configcntlrIP_lbl.text = controllerIPaddr

    if(validIPcheck(controllerIP_inp.text) == False):
        app.alert('Error: Invalid IP Address', 'The IP address is invalid! \n \'' + str(controllerIP_inp.text) + '\'\n was not recognized as a valid IP address.', 'warning')
    
    # username
    if controllerUser_inp.text:
        save_config('CONTROLLER', 'cntlrUser', controllerUser_inp.text)
        controllerUser = controllerUser_inp.text
        configcntlrUser_lbl.text = controllerUser

    # password
    if controllerPasswd_inp.text:
        save_config('CONTROLLER', 'cntlrPasswd', controllerPasswd_inp.text)
        controllerPasswd = controllerPasswd_inp.text
        configcntlrPasswd_lbl.text = controllerPasswd


    # duration
    if(controllerDuration_inp.text and controllerDuration_inp.text.isnumeric()):
        save_config('CONTROLLER', 'cntlrDuration', controllerDuration_inp.text)
        controllerDuration = controllerDuration_inp.text
        configcntlrDuration_lbl.text = controllerDuration

    if(controllerIP_inp.text or controllerUser_inp.text or controllerPasswd_inp.text or controllerDuration_inp.text):
        app.alert('Controller Settings Saved', 'Your changes have been saved.', 'info')
        controllerSetup.hide()
    
    updateGUI()

def open_addDoorsSetup(event):
    addDoorsSetup.show_on_top()

def open_remDoorsSetup(event):
    remDoorsSetup.show_on_top()

def addDoorsSetupSave(event):
    global doorsList
    ## if door ID is numeric check
    if addDoorID_inp.text.isnumeric() and addDoorName_inp.text not in doorsList:
        global doors
        doors = doors+1
        
        if(doors > 9):
            app.alert('Too Many Doors', 'The currently supported maximum amount of doors is nine (9).', 'error')
            doors = 9
        else:
            print('\ndoors has been added by one. doors is now equal to: {rDoorsw}'.format(rDoorsw=doors))
            save_config('DOORS', 'amount', '{rDOORNUM}'.format(rDOORNUM=doors)) # save how many doors we have
            save_config('DOORS', 'DOOR{doorNum}'.format(doorNum=doors), '{DOORNAME},{rDOORID}'.format(DOORNAME=addDoorName_inp.text, rDOORID=addDoorID_inp.text)) # save the actual door name and id as an array in the config
            
            app.alert('Door Added', str(addDoorName_inp.text) + ' has been added.', 'info')
            updateGUI()
            addDoorsSetup.hide()
    
    
    ## else if door name is in list check
    elif addDoorName_inp.text in doorsList:
        app.alert('Error: Invalid Door Name', 'The door name is invalid! \n \'' + str(addDoorName_inp.text) + '\'\n is already in use.', 'warning')
    else:
        app.alert('Error: Invalid Door ID', 'The door ID is invalid! \n \'' + str(addDoorID_inp.text) + '\'\n was not recognized as a valid door ID.', 'warning')
    

def remDoorsSetupSave(event):
    global doors
    doors = doors-1
    print('\ndoors has been subtracted by one. doors is now equal to: {rDoorsw}'.format(rDoorsw=doors))
    save_config('DOORS', 'amount', '{rDOORNUM}'.format(rDOORNUM=doors)) # save how many doors we have
    
    global doorsList
    
    rmDoorName = remDoorsSetup_listbox.remove_selected()
    rmDoorIDraw = doorsList.index(rmDoorName)
    rmDoorID = rmDoorIDraw+1 # get position in list of this door name, plus 1 to it since we're starting at 1 instead of 0 on our doors, whereas lists start at 0 traditionally
    
    print(rmDoorName, type(rmDoorName))
    print(rmDoorID, type(rmDoorID))
    print('door{rmID}'.format(rmID=rmDoorID))
    
    rem_config('DOORS', 'DOOR{rmID}'.format(rmID=rmDoorID))
    doorsList.remove(rmDoorName) # remove it from the actual list as well
    
    remDoorsSetup_listbox.select_none()
    updateGUI()

def updateGUI():
    read_config()
    
    #if running it normally in python, then use this:
    #os.startfile(__file__)
    #quit()
    
    #if using a pyinstaller .exe you should do this:
    os.startfile(sys.executable)
    sys.exit()

def open_config_frmMenu(event):
    webbrowser.open(CONFIG_FILE)

def open_config_folder(event):
    os.startfile(CONFIG_FILE_PATH)

def reset_config(event):
    if(app.confirm_okcancel('Reset Config', 'Are you sure you\'d like to reset your config?\n\nThis will remove ALL your doors and your Infinias Access Control server information.', 'warning') == True):
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            updateGUI()
        else:
            app.alert('Config File Doesn\'t Exist', 'Config File can not be reset as it does not exist.\nCheck \'AppData\Roaming\OpenSesame\' again for a configuration file.', 'error')

def tog_console_frmMenu(event):
    global console_togSwitch
    console_togSwitch = not console_togSwitch
    
    if(console_togSwitch):
        raise_console(True)
    else:
        raise_console(False)

# main app starting time
print('OpenSesame starting...\n')
raise_console(False)

# run the read_config function which will read from config and re-assign values to variables from the cfg
read_config()

# main window
app = gp.GooeyPieApp('OpenSesame')
app.width = 640
app.height = 480

needSetupMessage = gp.Label(app, 'Click on \'Setup\' to define door names and the controller\'s IP address')
    
app.add_menu_item('Setup', 'Controller', open_controllerSetup)
app.add_submenu_item('Setup', 'Doors', 'Add Door', open_addDoorsSetup)
app.add_submenu_item('Setup', 'Doors', 'Delete Door', open_remDoorsSetup)

app.add_menu_item('Advanced', 'Open Config', open_config_frmMenu)
app.add_menu_item('Advanced', 'Open Config Folder', open_config_folder)
app.add_menu_item('Advanced', 'Reset Config', reset_config)
app.add_menu_item('Advanced', 'Toggle Console', tog_console_frmMenu)

# nine door buttons for now, later this will  be capped at 24
door1Button = gp.Button(app, "Open\n{door1}".format(door1=door1Name), whichDoor)
door2Button = gp.Button(app, "Open\n{door2}".format(door2=door2Name), whichDoor)
door3Button = gp.Button(app, "Open\n{door3}".format(door3=door3Name), whichDoor)
door4Button = gp.Button(app, "Open\n{door4}".format(door4=door4Name), whichDoor)
door5Button = gp.Button(app, "Open\n{door5}".format(door5=door5Name), whichDoor)
door6Button = gp.Button(app, "Open\n{door6}".format(door6=door6Name), whichDoor)
door7Button = gp.Button(app, "Open\n{door7}".format(door7=door7Name), whichDoor)
door8Button = gp.Button(app, "Open\n{door8}".format(door8=door8Name), whichDoor)
door9Button = gp.Button(app, "Open\n{door9}".format(door9=door9Name), whichDoor)

app.set_grid(1, 1)

print('doors is equal to {rDoors}'.format(rDoors=doors))

# based on what's in our config, start making stuff look how it should
if doors == 0 or controllerIPaddr == '':
    app.add(needSetupMessage, 1, 1, align='center')

elif doors == 1:
    print('made it to elif statement, doors is equal to one!')
    app.set_grid(1, 1)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)

elif doors == 2:
    print('made it to elif statement, doors is equal to two!')
    app.set_grid(2, 1)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)

elif doors == 3:
    print('made it to elif statement, doors is equal to three!')
    app.set_grid(2, 2)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 1, 2, align='center', stretch=True, fill=True)

elif doors == 4:
    print('made it to elif statement, doors is equal to four!')
    app.set_grid(2, 2)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door4Button, 2, 2, align='center', stretch=True, fill=True)

elif doors == 5:
    print('made it to elif statement, doors is equal to five!')
    app.set_grid(3, 3)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 3, 1, align='center', stretch=True, fill=True)
    app.add(door4Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door5Button, 2, 2, align='center', stretch=True, fill=True)

elif doors == 6:
    print('made it to elif statement, doors is equal to six!')
    app.set_grid(3, 3)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 3, 1, align='center', stretch=True, fill=True)
    app.add(door4Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door5Button, 2, 2, align='center', stretch=True, fill=True)
    app.add(door6Button, 3, 2, align='center', stretch=True, fill=True)

elif doors == 7:
    print('made it to elif statement, doors is equal to seven!')
    app.set_grid(3, 3)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 3, 1, align='center', stretch=True, fill=True)
    app.add(door4Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door5Button, 2, 2, align='center', stretch=True, fill=True)
    app.add(door6Button, 3, 2, align='center', stretch=True, fill=True)
    app.add(door7Button, 1, 3, align='center', stretch=True, fill=True)

elif doors == 8:
    print('made it to elif statement, doors is equal to eight!')
    app.set_grid(3, 3)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 3, 1, align='center', stretch=True, fill=True)
    app.add(door4Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door5Button, 2, 2, align='center', stretch=True, fill=True)
    app.add(door6Button, 3, 2, align='center', stretch=True, fill=True)
    app.add(door7Button, 1, 3, align='center', stretch=True, fill=True)
    app.add(door8Button, 2, 3, align='center', stretch=True, fill=True)

elif doors == 9:
    print('made it to elif statement, doors is equal to nine!')
    app.set_grid(3, 3)
    app.add(door1Button, 1, 1, align='center', stretch=True, fill=True)
    app.add(door2Button, 2, 1, align='center', stretch=True, fill=True)
    app.add(door3Button, 3, 1, align='center', stretch=True, fill=True)
    app.add(door4Button, 1, 2, align='center', stretch=True, fill=True)
    app.add(door5Button, 2, 2, align='center', stretch=True, fill=True)
    app.add(door6Button, 3, 2, align='center', stretch=True, fill=True)
    app.add(door7Button, 1, 3, align='center', stretch=True, fill=True)
    app.add(door8Button, 2, 3, align='center', stretch=True, fill=True)
    app.add(door9Button, 3, 3, align='center', stretch=True, fill=True)

# controller setup window
controllerSetup = gp.Window(app, 'Controller Setup')
controllerSetup.width = 256
controllerSetup.height = 256
    
controllerIP_lbl = gp.Label(controllerSetup, "Intelli-M Access Control Server IP Address:")
controllerIP_inp = gp.Input(controllerSetup)
configcntlrIP_lbl = gp.Label(controllerSetup, controllerIPaddr)

controllerUser_lbl = gp.Label(controllerSetup, "Username:")
controllerUser_inp = gp.Input(controllerSetup)
configcntlrUser_lbl = gp.Label(controllerSetup, controllerUser)

controllerPasswd_lbl = gp.Label(controllerSetup, "Password:")
controllerPasswd_inp = gp.Input(controllerSetup)
configcntlrPasswd_lbl = gp.Label(controllerSetup, controllerPasswd)

controllerDuration_lbl = gp.Label(controllerSetup, "Duration to unlock:")
controllerDuration_inp = gp.Input(controllerSetup)
configcntlrDuration_lbl = gp.Label(controllerSetup, controllerDuration)



controllerSetupSave_btn = gp.Button(controllerSetup, 'Save', controllerSetupSave)
    
controllerSetup.set_grid(12,2)
controllerSetup.add(controllerIP_lbl, 1, 1)
controllerSetup.add(controllerIP_inp, 1, 2)
controllerSetup.add(configcntlrIP_lbl, 2, 2)

controllerSetup.add(controllerUser_lbl, 3, 1)
controllerSetup.add(controllerUser_inp, 3, 2)
controllerSetup.add(configcntlrUser_lbl, 4, 2)

controllerSetup.add(controllerPasswd_lbl, 6, 1)
controllerSetup.add(controllerPasswd_inp, 6, 2)
controllerSetup.add(configcntlrPasswd_lbl, 7, 2)

controllerSetup.add(controllerDuration_lbl, 9, 1)
controllerSetup.add(controllerDuration_inp, 9, 2)
controllerSetup.add(configcntlrDuration_lbl, 10, 2)

controllerSetup.add(controllerSetupSave_btn, 12, 2)

# adding doors window
addDoorsSetup = gp.Window(app, 'Add A Door')
addDoorsSetup.width = 256
addDoorsSetup.height = 256

addDoorName_lbl = gp.Label(addDoorsSetup, "Door Name:")
addDoorName_inp = gp.Input(addDoorsSetup)
addDoorID_lbl = gp.Label(addDoorsSetup, "Door RESTful API ID:")
addDoorID_inp = gp.Input(addDoorsSetup)
addDoorsSetupSave_btn = gp.Button(addDoorsSetup, 'Save', addDoorsSetupSave)

addDoorsSetup.set_grid(2,5)
addDoorsSetup.add(addDoorName_lbl, 1,1)
addDoorsSetup.add(addDoorName_inp, 1,2)
addDoorsSetup.add(addDoorID_lbl, 1,3)
addDoorsSetup.add(addDoorID_inp, 1,4)
addDoorsSetup.add(addDoorsSetupSave_btn, 2,5)

# deleting doors window
remDoorsSetup = gp.Window(app, 'Remove A Door')
remDoorsSetup.width = 256
remDoorsSetup.height = 256
remDoorsSetup.set_grid(2,3)

remDoorsSetup_lbl = gp.Label(remDoorsSetup, "Please choose the door you'd like to delete:")
remDoorsSetup_listbox = gp.Listbox(remDoorsSetup, doorsList)
remDoorsSetupSave_btn = gp.Button(remDoorsSetup, 'Save', remDoorsSetupSave)

remDoorsSetup.add(remDoorsSetup_lbl, 1, 1)
remDoorsSetup.add(remDoorsSetup_listbox, 1, 2, mulitple_selection=True, stretch=True, fill=True)
remDoorsSetup.add(remDoorsSetupSave_btn, 2, 3)

# run the GUI
try:
    app.run()
except(RuntimeError, TypeError, NameError, ValueError, SyntaxError, ZeroDivisionError, OSError, SystemError):
    raise_console(True)
    pause = input('\nThe message above is the error that caused the program to crash.')