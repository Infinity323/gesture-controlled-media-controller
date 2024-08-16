import os
import RGBFunctions
import RemoteDB

gestureOptions = ["Point Up", "Point Down", "Point Left", "Point Right", "Open Palm", "Closed Fist", "Peace Sign"]

remote = RemoteDB.getActiveRemote()
print("Using remote:",remote)

def sendButtonPress(protocol, buttonCode):
    startPulseLen = 9500
    if(protocol == "Samsung"):
        startPulseLen = 4500
    command = "sudo ./ir-slinger-master/IRSlinger -c " + buttonCode + " -l " + str(startPulseLen) + " -o 18"
    os.system(command)
    RGBFunctions.setLEDActive()

def buttonAction(gestureName):
    buttonData = RemoteDB.getKeyCode(remote, gestureName)
    if(buttonData != None):
        protocol = buttonData[2]
        code = buttonData[3]
        #print(code) 
        sendButtonPress(protocol, code)
    else:
        print("ERROR: Button for this gesture does not exist")

def destroy():
    command = "sudo killall pigpiod"
    os.system(command)

def powerAction():
    buttonAction(gestureOptions[6])
def upAction():
    buttonAction(gestureOptions[0])
def downAction():
    buttonAction(gestureOptions[1])
def leftAction():
    buttonAction(gestureOptions[2])
def rightAction():
    buttonAction(gestureOptions[3])
def pauseAction():
    buttonAction(gestureOptions[4])
def playAction():
    buttonAction(gestureOptions[4])
def muteAction():
    buttonAction(gestureOptions[5])