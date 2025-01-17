import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller, Key

# Initialize the video capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

# Initialize hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Keyboard settings
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

keyboard = Controller()

# Initialize variables
x_start = 100
y_start = 100
key_width = 65
key_height = 65
gap = 30

output_text = ""

# Space and Backspace button dimensions
space_x = 400
space_y = y_start + (key_height + gap) * 4  # Position below the keyboard
space_width = 200
space_height = 40

backspace_x = 650
backspace_y = space_y
backspace_width = 100
backspace_height = 40

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    # Draw base keyboard
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            x = x_start + j * (key_width + gap)
            y = y_start + i * (key_height + gap)
            cv2.rectangle(img, (x, y), (x + key_width, y + key_height),
                         (255, 255, 255), cv2.FILLED)
            cv2.putText(img, key, (x + 15, y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Draw Space button
    cv2.rectangle(img, (space_x, space_y),
                 (space_x + space_width, space_y + space_height),
                 (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "SPACE", (space_x + 70, space_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # Draw Backspace button
    cv2.rectangle(img, (backspace_x, backspace_y),
                 (backspace_x + backspace_width, backspace_y + backspace_height),
                 (255, 255, 255), cv2.FILLED)
    cv2.putText(img, "BACK", (backspace_x + 20, backspace_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            bbox = hand["bbox"]
            center = bbox[:2]

            if len(lmList) > 12:
                l, _, _ = detector.findDistance(
                    (lmList[8][0], lmList[8][1]),
                    (lmList[12][0], lmList[12][1]),
                    img
                )

                # Check for space button press
                if (space_x < center[0] < space_x + space_width and
                    space_y < center[1] < space_y + space_height):
                    if l < 50:
                        keyboard.press(Key.space)
                        cv2.rectangle(img, (space_x, space_y),
                                    (space_x + space_width, space_y + space_height),
                                    (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "SPACE", (space_x + 70, space_y + 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                        output_text += " "
                        sleep(0.50)

                # Check for backspace button press
                elif (backspace_x < center[0] < backspace_x + backspace_width and
                      backspace_y < center[1] < backspace_y + backspace_height):
                    if l < 50:
                        keyboard.press(Key.backspace)
                        cv2.rectangle(img, (backspace_x, backspace_y),
                                    (backspace_x + backspace_width, backspace_y + backspace_height),
                                    (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, "BACK", (backspace_x + 20, backspace_y + 30),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                        if len(output_text) > 0:
                            output_text = output_text[:-1]
                            sleep(0.50)

                # Check for regular key presses
                for i in range(len(keys)):
                    for j, key in enumerate(keys[i]):
                        x = x_start + j * (key_width + gap)
                        y = y_start + i * (key_height + gap)

                        if (x < center[0] < x + key_width and
                            y < center[1] < y + key_height):
                            cv2.rectangle(img, (x, y),
                                        (x + key_width, y + key_height),
                                        (175, 175, 175), cv2.FILLED)
                            cv2.putText(img, key, (x + 15, y + 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                            if l < 50:  # Clicking
                                keyboard.press(key)
                                cv2.rectangle(img, (x, y),
                                            (x + key_width, y + key_height),
                                            (0, 255, 0), cv2.FILLED)
                                cv2.putText(img, key, (x + 15, y + 30),
                                          cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                                output_text += key
                                sleep(0.50)

    # Draw output rectangle
    cv2.rectangle(img, (100, 550), (1000, 600), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, f"Output: {output_text}", (110, 575),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)


    cv2.imshow("Virtual Keyboard", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

