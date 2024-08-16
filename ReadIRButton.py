# Derived from https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/
import RPi.GPIO as GPIO
import math
from datetime import datetime

INPUT_WIRE = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_WIRE, GPIO.IN)

# Reads raw IR data and returns list of pulses
def scanIR():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_WIRE, GPIO.IN)
    prevValue = 1 #Previvous value read
    fallEdgeTime = datetime.now() # Falling edge timestamp
    riseEdgeTime = datetime.now()
    pulseList = [] # Stores pulse data (high or low and time it was high or low)
    while True:
        # Active low (A high pulse will read as 0, low as 1)
        value = GPIO.input(INPUT_WIRE)
        
        # Found rising edge, save time input was low to pulseList
        if(value == 0 and prevValue == 1):
            fallEdgeTime = datetime.now()
            prevValue = 0
            timeDelta = (fallEdgeTime - riseEdgeTime)
            timeDelta = int(timeDelta.microseconds)
            #print("L",timeDelta)
            pulseList.append([0,timeDelta])
        
        # Found falling edge, save time input was high to pulseList
        elif(value == 1 and prevValue == 0):
            riseEdgeTime = datetime.now()
            prevValue = 1
            timeDelta = (riseEdgeTime - fallEdgeTime)
            timeDelta = int(timeDelta.microseconds)
            #print("H",timeDelta)
            pulseList.append([1,timeDelta])

        # Done reading button, return list of pulseList
        if(len(pulseList) > 32 and ((datetime.now() - riseEdgeTime).seconds) > 0.1):
            print("Got",len(pulseList),"pulses")
            return pulseList

# Analyze list of pulses and determine if data is high or low
def analyzePulses(pulseList):
    # Check for protocol
    protocol = "NS"
    startPulseHigh = pulseList[1][1]
    startPulseLow = pulseList[2][1]
    if(startPulseHigh > 8000 and startPulseHigh < 10000 and startPulseLow > 4000 and startPulseLow < 5000):
        print("NEC protocol detected")
        protocol = "NEC"
    elif(startPulseHigh > 4000  and startPulseHigh < 5000 and startPulseLow > 4000 and startPulseLow < 5000):
        print("Samsung protocol detected")
        protocol = "Samsung"
    else:
        print("ERROR: remote using unsupported protocol")
        return -1

    buttonCode = "" # Store button code in binary
    errorBit = False # Set true if a bit for button code had error
    i = 3 #ignore first 3 indexes (wait for pulse, NEC high check, NEC low check)

    # Loop thru pulse data
    while(i < len(pulseList)-1):
        pulseLength = pulseList[i][1] #High time
        pulseGap = pulseList[i+1][1] #Low time
       
        # Error Checking
        pulseHighCheck = pulseList[i][0]
        pulseLowCheck = pulseList[i+1][0]
        if(pulseHighCheck == 0):
            print("ERROR: Got Low Pulse, Expected High")
            errorBit = True
        if(pulseLowCheck == 1):
            print("ERROR: Got High Pulse, Expected Low")
            errorBit = True
        if(pulseLength > 1000):
            print("ERROR: High Pulse Too Long:",pulseLength)
            errorBit = True
        if(pulseGap > 2000):
            print("ERROR: Pulse Gap Too Long:",pulseGap)
            errorBit = True
       
        # Characterize Data (ignore error bits)
        if(errorBit == False):
            if(pulseGap > 1000):
                buttonCode += "1"
            else:
                buttonCode += "0"
        errorBit = False
        i += 2
    print("Raw Button Code:",buttonCode)

    # Button code must have power of 2 number of bits
    if(math.log2(len(buttonCode)).is_integer):
        if(protocol == "Samsung" and len(buttonCode) == 64):
            buttonCode = buttonCode[0:32]
        return protocol, buttonCode
    print("ERROR: Button code must have power of 2 number of bits, got", len(buttonCode))
    return -1

def getButtonCode():
    pulseList = scanIR()
    return analyzePulses(pulseList)