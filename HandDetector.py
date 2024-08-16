import cv2
import mediapipe as mp

"""
Hand Detector class.
Facilitates organization of MediaPipe function calls
"""
class HandDetector():
    """
    Constructor
    """
    def __init__(self, image_mode = False, max_hands = 1, min_detect_con = 0.5, min_track_con = 0.5):
        # Configuration options
        self.image_mode = image_mode
        self.max_hands = max_hands
        self.min_detect_con = min_detect_con
        self.min_track_con = min_track_con
        # Instantatiate MediaPipe Hands object
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            self.image_mode,
            self.max_hands,
            self.min_detect_con,
            self.min_track_con)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
    
    """
    Process hand landmarks and (optionally) draw hand landmarks on the frame
    """
    def findHands(self, img, draw = True):
        # Speed up performance
        img.flags.writeable = False
        # Convert color from BGR to RGB
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Process hand landmarks
        self.results = self.hands.process(img_RGB)
        # Check if hand landmarks found
        if self.results.multi_hand_landmarks:
            if draw:
                for hand_landmarks in self.results.multi_hand_landmarks:
                    # Draw hand landmarks on image
                    self.mp_drawing.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS, self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style())
        
        return img

    """
    Return list of hand landmark positions
    """
    def findPosition(self, img, hand_no = 0, draw = True):
        # Create list of hand landmark positions
        lm_list = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, _ = img.shape
                # Save coordinates relative to window size
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        
        return lm_list

    """
    Return enumerated list of hand landmarks
    """
    def getHandLandmarks(self):
        # https://google.github.io/mediapipe/images/mobile/hand_landmarks.png
        return self.mp_hands.HandLandmark