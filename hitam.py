import cv2
import numpy as np

# Function to do nothing (needed for creating trackbars)
def nothing(x):
    pass

# Create a window named 'image' and open it
cv2.namedWindow('image')

# Create trackbars for HSV color range
cv2.createTrackbar('Hue Min', 'image', 0, 179, nothing)
cv2.createTrackbar('Hue Max', 'image', 0, 179, nothing)
cv2.createTrackbar('Saturation Min', 'image', 0, 255, nothing)
cv2.createTrackbar('Saturation Max', 'image', 0, 255, nothing)
cv2.createTrackbar('Value Min', 'image', 0, 255, nothing)
cv2.createTrackbar('Value Max', 'image', 0, 255, nothing)

# Set initial values for trackbars
cv2.setTrackbarPos('Hue Min', 'image', 0)
cv2.setTrackbarPos('Hue Max', 'image', 179)
cv2.setTrackbarPos('Saturation Min', 'image', 0)
cv2.setTrackbarPos('Saturation Max', 'image', 255)
cv2.setTrackbarPos('Value Min', 'image', 0)
cv2.setTrackbarPos('Value Max', 'image', 255)

# Capture video from default camera
cap = cv2.VideoCapture(-1)

while True:
    # Read frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # frame = cv2.imread('1.jpg',1)
    frame = cv2.resize(frame,(640,480))
    frame = cv2.flip(frame,0)
    frame = cv2.flip(frame,1)
    # Convert frame from BGR to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Get current positions of all trackbars
    h_min = cv2.getTrackbarPos('Hue Min', 'image')
    h_max = cv2.getTrackbarPos('Hue Max', 'image')
    s_min = cv2.getTrackbarPos('Saturation Min', 'image')
    s_max = cv2.getTrackbarPos('Saturation Max', 'image')
    v_min = cv2.getTrackbarPos('Value Min', 'image')
    v_max = cv2.getTrackbarPos('Value Max', 'image')
    
    # Define the lower and upper bounds of the HSV color range
    lower_bound = np.array([h_min, s_min, v_min])
    upper_bound = np.array([h_max, s_max, v_max])

    # Threshold the HSV image to get only colors in the specified range
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the original frame and the mask
    cv2.imshow('image', np.hstack([frame, res]))
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
