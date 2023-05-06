import config
from tkinter import *

from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC

global serverStatusTextLabel
global selectedTrack
    
trackList = [
    'paul_ricard',
    'misano',
    'nurburgring',
    'hungaroring',
    'zolder',
    'monza',
    'brands_hatch',
    'spa',
    'silverstone',
    'barcelona',
    'zandvoort',
    'kyalami_2019',
    'mount_panorama_2019',
    'laguna_seca_2019',
    'suzuka_2019',
    'imola_2020',
    'barcelona_2020',
    'spa_2020',
    'paul_ricard_2020',
    'monza_2019',
    'zolder_2019',
    'brands_hatch_2019',
    'silverstone_2019',
    'paul_ricard_2019',
    'misano_2019',
    'spa_2019',
    'nurburgring_2019',
    'barcelona_2019',
    'hungaroring_2019',
    'zandvoort_2019',
    'monza_2020',
    'zolder_2020',
    'brands_hatch_2020',
    'silverstone_2020',
    'misano_2020',
    'nurburgring_2020',
    'hungaroring_2020',
    'zandvoort_2020',
    'donington_2019',
    'oulton_park_2019',
    'snetterton_2019',
    'cota',
    'indianapolis',
    'watkins_glen'
]

#initialize the driver
def initDriver():
    global driver    
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("window-size=1920,1080")
    option.add_argument("--log-level=3") 
    driver = webdriver.Chrome(options=option)
    driver.get('https://cp.elitegameservers.net/Login')

# function to handle the login screen
def loginToScreen():
    # find necessary elements
    userNameBox = driver.find_element(By.CSS_SELECTOR, '#UserName')
    passwordBox = driver.find_element(By.CSS_SELECTOR, '#Password')
    loginButton = driver.find_element(By.CSS_SELECTOR, '#loginButton')

    # send login info
    userNameBox.send_keys(config.userName)
    passwordBox.send_keys(config.password)

    loginButton.click()
    serverStatusTextLabel = 'Login Success'
    print(serverStatusTextLabel)

    # could be better couldn't find a way to click dropdown menu.
    # driver.get('https://cp.elitegameservers.net/Interface/Game/GameServers')


# get to the config files page
def getToConfigFiles():
    configFiles = driver.find_element(By.CSS_SELECTOR, '#main > div.detail > div > div:nth-child(1)')
    configFiles.click()
    serverStatusTextLabel = "Configuration Files Success"
    print(serverStatusTextLabel)


# open the config editor
def openEditor():
    configEditor = driver.find_element(By.CSS_SELECTOR, '#ConfigFilesGrid > table > tbody > tr:nth-child(3) > td.k-command-cell.k-command-cell.k-command-cell.k-command-cell > a.k-button.k-button-icontext.k-grid-ConfigEditor')
    configEditor.click()
    serverStatusTextLabel = "Open Editor Success"
    print(serverStatusTextLabel)

# change the name of the track
def changeTrackSelection(trackName):
    # change iframe to the popup window
    driver.switch_to.frame('ifilecontents')
    trackOptions = Select(driver.find_element(By.CSS_SELECTOR, '#ContentPlaceHolderMain_MvcConfigEditor1_FormViewer1_ComboBox14413_DropDownList1'))
    trackOptions.select_by_value(trackName) # use visible track name to select the track. could be switched to value or others
    serverStatusTextLabel = 'Track Changed Success'
    print(serverStatusTextLabel)
    print(f'Track Changed to {trackName}')

# save changes made to the server
def saveChanges():
    driver.switch_to.default_content()
    saveButton = driver.find_element(By.CSS_SELECTOR, '#saveCloseButton')
    saveButton.click()
    serverStatusTextLabel = 'Save Success'
    print(serverStatusTextLabel)

# to go back to the homepage -- could also be simplified to just go to the homepage instead of waiting for the element to be clickable 
#simplify the function below
def toHomePage():
    driver.get('https://cp.elitegameservers.net/Interface/Game/GameServers')
# def toHomeOriginal():
#an original version of the function that waits for the element to be clickable before clicking it, very prone to error, slow, and not necessary simplified above.
#     WebDriverWait(driver, timeout=7).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#ServiceHomeLink > div > span")))
#     homeLink = driver.find_element(By.CSS_SELECTOR,"#ServiceHomeLink > div > span")
#     homeLink.click()
#     serverStatusTextLabel = 'Home Success'
#     print(serverStatusTextLabel)


# click the restart server button
def restartServer():
    restartButton = driver.find_element(By.CSS_SELECTOR, '#Restart')
    restartButton.click()
    serverStatusTextLabel = "Server Restarted"
    print(serverStatusTextLabel)

# change the server to the track name
def changeTrack(trackName):
    initDriver()
    loginToScreen()
    getToConfigFiles()
    openEditor()
    changeTrackSelection(trackName)
    saveChanges()
    toHomePage()
    restartServer()
    print(f'Track Change Complete. Changed to {trackName}')
    driver.quit()

root = Tk()
root.title("ACC Track Updater")

# Add a grid
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.pack(pady=(25, 50), padx=100)

# Create a Tkinter variable
tkvar = StringVar(root)

# Dictionary with options
tkvar.set(trackList[0])  # set the default option

popupMenu = OptionMenu(mainframe, tkvar, *trackList)
Label(mainframe, text="Choose a track:").grid(row=1, column=1)
popupMenu.grid(row=2, column=1)

# on change dropdown value
def change_dropdown(*args):
    global selectedTrack
    selectedTrack = tkvar.get()
    # print(selectedTrack)

changeTrackButton = Button(root, text="Change Server", command=lambda: changeTrack(selectedTrack))
changeTrackButton.pack(anchor=CENTER, padx=10, pady=(10, 50))

# link function to change dropdown
tkvar.trace('w', change_dropdown)

root.mainloop()
