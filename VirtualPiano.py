import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load piano sounds
piano_sounds = [
    pygame.mixer.Sound("sounds/a6.mp3"),
    pygame.mixer.Sound("sounds/b6.mp3"),
    pygame.mixer.Sound("sounds/c6.mp3"),
    pygame.mixer.Sound("sounds/c3.mp3"),
    pygame.mixer.Sound("sounds/d6.mp3"),
    pygame.mixer.Sound("sounds/do.mp3"),
    pygame.mixer.Sound("sounds/e6.mp3"),
    pygame.mixer.Sound("sounds/f6.mp3"),
    pygame.mixer.Sound("sounds/fa.mp3"),
    pygame.mixer.Sound("sounds/g6.mp3"),
    pygame.mixer.Sound("sounds/la.mp3"),
    pygame.mixer.Sound("sounds/fa.mp3"),
    pygame.mixer.Sound("sounds/mi.mp3"),
    pygame.mixer.Sound("sounds/re.mp3"),
    pygame.mixer.Sound("sounds/si.mp3"),
]

# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Piano key settings
keys = [['A6', 'B6', 'C6', 'C3', 'D3', 'Do', 'E6'],
        ['F6', 'Fa', 'G6', 'La', 'Fa', 'Mi', 'Re', 'Si']]
key_width = 120
key_height = 150
x_start = 100
y_start = 100
row_gap = 20

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw piano keys
    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            x = x_start + col_idx * key_width
            y = y_start + row_idx * (key_height + row_gap)
            cv2.rectangle(img, (x, y), (x + key_width, y + key_height),
                          (255, 255, 255, 50), cv2.FILLED)  # Transparent fill
            cv2.rectangle(img, (x, y), (x + key_width, y + key_height),
                          (0, 0, 0), 2)  # Border
            cv2.putText(img, key, (x + 20, y + key_height - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            bbox = hand["bbox"]
            center = bbox[:2]

            if len(lmList) > 8:
                l, _, _ = detector.findDistance(
                    (lmList[8][0], lmList[8][1]),
                    (lmList[12][0], lmList[12][1]),
                    img
                )

                # Check for key presses
                for row_idx, row in enumerate(keys):
                    for col_idx, key in enumerate(row):
                        x = x_start + col_idx * key_width
                        y = y_start + row_idx * (key_height + row_gap)

                        if (x < center[0] < x + key_width and
                            y < center[1] < y + key_height):

                            cv2.rectangle(img, (x, y), (x + key_width, y + key_height),
                                          (0, 255, 0, 50), cv2.FILLED)  # Highlight transparent
                            cv2.putText(img, key, (x + 20, y + key_height - 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

                            if l < 50:  # Clicking
                                index = row_idx * len(keys[0]) + col_idx
                                piano_sounds[index].play()
                                sleep(0.5)  # Prevent multiple quick presses

    cv2.imshow("Virtual Piano", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
