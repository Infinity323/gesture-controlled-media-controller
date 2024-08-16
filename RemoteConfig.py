import RPi.GPIO as GPIO
import ReadIRButton
import RemoteDB

gestureOptions = ["Point Up", "Point Down", "Point Left", "Point Right", "Open Palm", "Closed Fist", "Peace Sign"]

# Get button code
def addNewButton(gestureName):
    # Get 2 button presses and make sure the codes match
    print("Please press the key you want to map to \"" + gestureName + "\"")
    buttonCode1 = ReadIRButton.getButtonCode()
    print("Please press the key again")
    buttonCode2 = ReadIRButton.getButtonCode()
    if(buttonCode1 == buttonCode2):
        print("Success")
    else: # If no match, keep retrying
        match = False
        while(match == False):
            print("ERROR: Button codes did not match. Please try again")
            print("Please press the key you want to map to \"" + gestureName + "\"")
            buttonCode1 = ReadIRButton.getButtonCode()
            print("Please press key again")
            buttonCode2 = ReadIRButton.getButtonCode()
            if(buttonCode1 == buttonCode2):
                print("Success")
                match = True
    return buttonCode1

# Select remote to modify
def selectRemote(setActive):
    # Display possible remotes
    remotes = RemoteDB.getRemoteNames()
    for i in range(len(remotes)):
        print(str(i+1) + ":",remotes[i])
    # Get remote option
    choice = int(input("Line number: "))
    if(len(remotes) == 0):
        print("No remotes exist")
        return -1
    elif(choice >= 1 and choice <= len(remotes)):
        print(remotes[choice-1], "selected")
        # Update active remote if setActive True
        if(setActive):
            RemoteDB.setActiveRemote(remotes[choice-1])
    else: # Invalid option
        print("ERROR: Invalid line number")
        return None
    return remotes[choice-1]

# Add new remote or buttons to database
def addRemote(remoteName):
    remoteData = [] # Array of remote data with name, protocol, button name and code
    # Get nae of remote
    if(remoteName == ""):
        remoteName = input("Enter a name for the remote: ")
    while(True):
        # Get line number for desired gesture
        print("\nSelect the line number for the gesture you want to add.\nEnter any other number to quit.")
        for i in range(len(gestureOptions)):
            print(str(i+1) + ":",gestureOptions[i])
        gestureChoice = int(input("Line number: "))
        # Call addNewButton to sync button and gesture
        if(gestureChoice >= 1 and gestureChoice <= len(gestureOptions)):
            # Get the buttons code from IR receiver and save data to array
            code = addNewButton(gestureOptions[gestureChoice-1])
            if(code == -1):
                print("ERROR: Could not parse button code")
                return -1
            keyData = (remoteName, gestureOptions[gestureChoice-1], code[0], code[1], remoteName + "-" + gestureOptions[gestureChoice-1])
            remoteData.append(keyData)
            print(keyData)
        elif (len(remoteData) > 0): # Done with adding buttons, so add them to databse
            RemoteDB.addButtons(remoteData)
            return
        else:
            return

# View and edit a remote        
def editRemote():
    # Get remore user wants to change
    print("\nSelect the line number for the remote you want to edit")
    remoteName = selectRemote(False)
    # Prompt for action
    print("\nSelect the line number for the action you want to do")
    print("1: Show configured buttons")
    print("2: Add a button")
    print("3: Remove a button")
    print("4: Remove remote")
    choice = int(input("Line number:"))
    if (choice == 1): # Show list of configured buttons for remote
        buttons = RemoteDB.showConfiguredButtons(remoteName)
        for i in range(len(buttons)):
            print(buttons[i][1])
    elif(choice == 2): # Add a new button to remote
        addRemote(remoteName)
    elif (choice == 3): # Remove a gesture
        # Prompt user
        print("\nSelect the line number for the gesture you want to remove. Enter any other number to cancel.")
        for i in range(len(gestureOptions)):
            print(i+1,":",gestureOptions[i])
        gestureChoice = int(input("Line number: "))
        if(gestureChoice >= 1 and gestureChoice <= len(gestureOptions)):
            # Make SQL command and update DB
            keyName = gestureOptions[gestureChoice - 1]
            sqlCommand  = "DELETE FROM Remotes WHERE remoteName= '" + remoteName + "' AND keyName='" + keyName + "' "
            RemoteDB.updateDB(sqlCommand)
        else:
            return
    elif (choice == 4): # Dlete entire remote (require extra conformation)
        print("This will delete the remote from the database. Enter 'Y' if sure or 'n' to cancel")
        choice = input("Y/n: ")
        if(choice == "Y"):
            sqlCommand  = "DELETE FROM Remotes WHERE remoteName= '" + remoteName + "'"
            RemoteDB.updateDB(sqlCommand)
        else:
            return
    else:
        # Invalid option
        print("ERROR: Invalid option")
        return

def main():
    try:
        while(True):
            print("\nPlease select a line number. Input any other number to quit.")
            print("1: Set active remote")
            print("2: Show active remote")
            print("3: Add new remote")
            print("4: Edit/ View remote")
            print("5: Show database")
            choice = int(input("Line number: "))
            if(choice >= 1 and choice <= 5):
                if(choice == 1):
                    print("\nSelect line number for remote you want to activate")
                    selectRemote(True)
                elif(choice == 2):
                    print("\nActive remote:",RemoteDB.getActiveRemote())
                elif(choice == 3):
                    addRemote("")
                elif(choice == 4):
                    editRemote()
                elif(choice == 5):
                    RemoteDB.showDB()
                else:
                    quit()
            else:
                GPIO.cleanup()
                quit()
    # Catch CTRL-C
    except KeyboardInterrupt:
        GPIO.cleanup()
        quit()

if __name__ == "__main__":
    main()

# TODO override code of button name same in update function