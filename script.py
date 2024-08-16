import cv2
import time
import math
import statistics
import threading

import HandDetector as HD
import IRFunctions
import RGBFunctions

# Global variables
GUESSES = 4
guesses = []

"""
Based on most frequently detected gestures, choose the command
"""
def doCommand():
    try:
        # Perform command based on most-guessed gesture
        gesture = statistics.mode(guesses)
        if gesture == "pointing up":
            print("VOLUME UP")
            IRFunctions.upAction()
        elif gesture == "pointing down":
            print("VOLUME DOWN")
            IRFunctions.downAction()
        elif gesture == "pointing left":
            print("BACK")
            IRFunctions.leftAction()
            time.sleep(2)
        elif gesture == "pointing right":
            print("FORWARD")
            IRFunctions.rightAction()
            time.sleep(2)
        elif gesture == "open palm":
            print("PAUSE")
            IRFunctions.pauseAction()
            time.sleep(2)
        elif gesture == "closed fist":
            print("MUTE")
            IRFunctions.muteAction()
            time.sleep(2)
        elif gesture == "peace sign":
            print("POWER")
            IRFunctions.powerAction()
            time.sleep(3)
    # If no mode detected
    except statistics.StatisticsError:
        # Clear guesses
        guesses.clear()

    # Clear guesses
    guesses.clear()
    RGBFunctions.setLEDReady()

    return

"""
Determines gesture based on hand landmark positions.
Only compatible with right hand!
"""
def determineGesture(lm_list, lm_enum, hand_size):
    # Tolerance to differentiate between gestures (depends on hand size)
    tolerance = hand_size * 0.3
    # Determine gesture based on hand landmark positions
    if (lm_list[lm_enum.THUMB_TIP][1] >= lm_list[lm_enum.THUMB_CMC][1] and
        lm_list[lm_enum.INDEX_FINGER_TIP][2] <= lm_list[lm_enum.INDEX_FINGER_MCP][2]  and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][2] <= lm_list[lm_enum.MIDDLE_FINGER_DIP][2] and
        lm_list[lm_enum.RING_FINGER_TIP][2] <= lm_list[lm_enum.RING_FINGER_DIP][2] and
        lm_list[lm_enum.PINKY_TIP][2] <= lm_list[lm_enum.PINKY_DIP][2]):
        guesses.append("open palm")
    elif (lm_list[lm_enum.THUMB_TIP][1] <= lm_list[lm_enum.THUMB_IP][1] and
        lm_list[lm_enum.INDEX_FINGER_TIP][2] <= lm_list[lm_enum.INDEX_FINGER_MCP][2] - tolerance and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][2] <= lm_list[lm_enum.MIDDLE_FINGER_MCP][2] - tolerance and
        lm_list[lm_enum.RING_FINGER_TIP][2] >= lm_list[lm_enum.RING_FINGER_PIP][2] and
        lm_list[lm_enum.PINKY_TIP][2] >= lm_list[lm_enum.PINKY_PIP][2] and
        lm_list[lm_enum.INDEX_FINGER_MCP][2] <= lm_list[lm_enum.WRIST][2]):
        guesses.append("peace sign")
    elif (lm_list[lm_enum.THUMB_TIP][1] <= lm_list[lm_enum.THUMB_IP][1] and
        lm_list[lm_enum.INDEX_FINGER_TIP][2] >= lm_list[lm_enum.INDEX_FINGER_PIP][2] and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][2] >= lm_list[lm_enum.MIDDLE_FINGER_PIP][2] and
        lm_list[lm_enum.RING_FINGER_TIP][2] >= lm_list[lm_enum.RING_FINGER_PIP][2] and
        lm_list[lm_enum.PINKY_TIP][2] >= lm_list[lm_enum.PINKY_PIP][2] and
        lm_list[lm_enum.INDEX_FINGER_MCP][2] <= lm_list[lm_enum.WRIST][2]):
        guesses.append("closed fist")
    elif (lm_list[lm_enum.INDEX_FINGER_TIP][2] <= lm_list[lm_enum.INDEX_FINGER_MCP][2] - tolerance and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][2] >= lm_list[lm_enum.MIDDLE_FINGER_DIP][2] and
        lm_list[lm_enum.RING_FINGER_TIP][2] >= lm_list[lm_enum.RING_FINGER_DIP][2] and
        lm_list[lm_enum.PINKY_TIP][2] >= lm_list[lm_enum.PINKY_DIP][2]):
        guesses.append("pointing up")
    elif (lm_list[lm_enum.INDEX_FINGER_TIP][2] >= lm_list[lm_enum.INDEX_FINGER_MCP][2] + tolerance and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][2] <= lm_list[lm_enum.MIDDLE_FINGER_DIP][2] and
        lm_list[lm_enum.RING_FINGER_TIP][2] <= lm_list[lm_enum.RING_FINGER_DIP][2] and
        lm_list[lm_enum.PINKY_TIP][2] <= lm_list[lm_enum.PINKY_DIP][2]):
        guesses.append("pointing down")
    elif (lm_list[lm_enum.INDEX_FINGER_TIP][1] >= lm_list[lm_enum.INDEX_FINGER_MCP][1] and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][1] <= lm_list[lm_enum.MIDDLE_FINGER_DIP][1] and
        lm_list[lm_enum.RING_FINGER_TIP][1] <= lm_list[lm_enum.RING_FINGER_DIP][1] and
        lm_list[lm_enum.PINKY_TIP][1] <= lm_list[lm_enum.PINKY_DIP][1]):
        guesses.append("pointing left")
    elif (lm_list[lm_enum.INDEX_FINGER_TIP][1] <= lm_list[lm_enum.INDEX_FINGER_MCP][1] and
        lm_list[lm_enum.MIDDLE_FINGER_TIP][1] >= lm_list[lm_enum.MIDDLE_FINGER_DIP][1] and
        lm_list[lm_enum.RING_FINGER_TIP][1] >= lm_list[lm_enum.RING_FINGER_DIP][1] and
        lm_list[lm_enum.PINKY_TIP][1] >= lm_list[lm_enum.PINKY_DIP][1]):
        guesses.append("pointing right")
    # else:
    #     print("unknown")

    return


"""
Main program loop.
"""
def driver(previous_time, current_time, video_capture, hand_detector, lm_enum, hand_size):
    while video_capture.isOpened():
        _, img = video_capture.read()
        img = hand_detector.findHands(img)
        lm_list = hand_detector.findPosition(img)
        if len(lm_list) != 0:
            hand_size = math.sqrt((lm_list[lm_enum.INDEX_FINGER_TIP][1] - lm_list[lm_enum.WRIST][1])**2 + (lm_list[lm_enum.INDEX_FINGER_TIP][2] - lm_list[lm_enum.WRIST][2])**2)
            guess_thread = threading.Thread(target=determineGesture, args=(lm_list, lm_enum, hand_size), daemon=True)
            guess_thread.start()

        # Calculate FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Show live image feed
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 255), 3)
        cv2.imshow("Image", cv2.flip(img, 1))
        cv2.waitKey(1)

        if (len(guesses) == GUESSES):
            command_thread = threading.Thread(target=doCommand, daemon=True)
            command_thread.start()


def main():
    previous_time = 0
    current_time = 0
    video_capture = cv2.VideoCapture(0)
    hand_detector = HD.HandDetector()
    lm_enum = hand_detector.getHandLandmarks()
    hand_size = 0

    # Initialize program
    try:
        RGBFunctions.init()
        RGBFunctions.setLEDReady()
        driver(previous_time, current_time, video_capture, hand_detector, lm_enum, hand_size)
    # Catch CTRL-C
    except KeyboardInterrupt:
        video_capture.release()
        RGBFunctions.destroy()
        IRFunctions.destroy()
    
    return


if __name__ == "__main__":
    main()