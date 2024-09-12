import numpy as np
import cv2
from skimage.filters.rank import median
from skimage.morphology import disk

# Path to the image
frame = cv2.imread('C:/Users/emman/OneDrive - Instituto Federal de Santa Catarina/IFSC/DSP II - Carlos Speranza/trabalho final/1.jpg')

# Resize the image to HD resolution (1440x1080)
frame = cv2.resize(frame, (1440, 1080))

# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Define the color range for the mask
lower = np.array([0, 20, 120])
upper = np.array([180, 230, 255])

# Create the mask and reduce noise using a median filter with a radius of 20
mask = cv2.inRange(hsv, lower, upper)
mask = median(mask, disk(20))

# Bitwise-AND between the mask and the original image
res = cv2.bitwise_and(frame, frame, mask=mask)
cv2.imshow('Separated Potatoes', res)

# Set area thresholds for classification
small_threshold = 30000
medium_threshold = 60000

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# List to store information about each object
objects_info = []

# Iterate over the contours
for i, contour in enumerate(contours):
    # Calculate the contour area
    area = cv2.contourArea(contour)

    # Classify the contour based on its area
    if area < small_threshold:
        classification = 'Small'
    elif area < medium_threshold:
        classification = 'Medium'
    else:
        classification = 'Large'

    # Get the bounding rectangle coordinates
    x, y, w, h = cv2.boundingRect(contour)

    # Add information to the list
    objects_info.append({'Classification': classification, 'Area': area, 'Location': (x, y, w, h)})

    # Draw contour and label on the image
    cv2.drawContours(res, [contour], -1, (0, 255, 0), 2)  # Green contour
    cv2.putText(res, classification, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

# Show the image with labels
cv2.imshow('Object Classification', res)
cv2.imshow('Mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Return object information
for i, obj_info in enumerate(objects_info):
    print(f"Object {i+1} - Classification: {obj_info['Classification']}, Area: {obj_info['Area']} square pixels, Location: {obj_info['Location']}")
