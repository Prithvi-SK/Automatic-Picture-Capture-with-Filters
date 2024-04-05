import cv2
import mediapipe as mp
import time
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0) # select webcam

# Initialize initial_count and capture_frame to None
initial_count = None
capture_frame = None

# Function to check if mouse is clicked on the button
def button_clicked(event, x, y, flags, param):
    global initial_count
    if event == cv2.EVENT_LBUTTONDOWN:
        initial_count = 5  # Set initial_count to 5 to start counting fingers

# Create a window to display the button
cv2.namedWindow('Start Counting Fingers')
cv2.setMouseCallback('Start Counting Fingers', button_clicked)

# Display button and wait for user to click
while True:
    # Create a black image
    button_image = np.zeros((300, 600, 3), dtype=np.uint8)

    # Draw the button
    cv2.rectangle(button_image, (100, 100), (500, 200), (255, 255, 255), thickness=2)
    cv2.putText(button_image, 'Start Counting Fingers', (130, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display the image
    cv2.imshow('Start Counting Fingers', button_image)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Check if user clicked the button
    if initial_count is not None:
        break

# Close the window
cv2.destroyWindow('Start Counting Fingers')

# Start hand tracking
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    start_time = time.time()
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Check if hand(s) detected and initial_count is not None
        if initial_count is not None and results.multi_hand_landmarks:
            # loop through hands
            for hand_landmarks in results.multi_hand_landmarks:
                # get hand landmarks
                landmarks = hand_landmarks.landmark
                # count fingers
                thumb = landmarks[4].y < landmarks[3].y < landmarks[2].y < landmarks[1].y
                index = landmarks[8].y < landmarks[7].y < landmarks[6].y < landmarks[5].y
                middle = landmarks[12].y < landmarks[11].y < landmarks[10].y < landmarks[9].y
                ring = landmarks[16].y < landmarks[15].y < landmarks[14].y < landmarks[13].y
                pinky = landmarks[20].y < landmarks[19].y < landmarks[18].y < landmarks[17].y
                fingers = [thumb, index, middle, ring, pinky]
                count = fingers.count(True)

                # Store the first recorded value greater than 0 of count in initial_count
                if initial_count is None and count > 0:
                    initial_count = count

                # Decrement initial_count every second
                elapsed_time = time.time() - start_time
                if elapsed_time >= 1:
                    start_time = time.time()
                    if initial_count is not None:
                        initial_count = max(initial_count - 1, 0)

                # Capture the frame when initial_count reaches 0
                if initial_count ==  0 and capture_frame is None:
                    capture_frame = image.copy()
                    cv2.imshow('Captured Frame', capture_frame)

                # Display finger count on image
                cv2.putText(image, f'Finger Count: {count}', (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # Draw hand landmarks on image
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the resulting image
        cv2.imshow('Hand Tracking', image)

        # Exit on pressing 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows
