import cv2 
import numpy as np
import math
import statistics as st

def crop(image):
    raw_min = 130 # TODO: Implement a non hard-coded value
    
    # -- Layer 1 --
    
    # Intense Blur
    blurred = cv2.GaussianBlur(image, (((math.ceil((image.shape[0])/2)+(1 - (image.shape[0]) % 2))), ((math.ceil((image.shape[1])/2)+(1 - (image.shape[1]) % 2)))), 0) 
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY) # Convert to greyscale
    thresh = cv2.threshold(gray, raw_min, 255, cv2.THRESH_BINARY)[1] # Threshold operation
    contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0] # Find contours of the threshold image
    
    # Find the largest contour
    max_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]

    # L1 Rectangle
    rect = cv2.minAreaRect(max_contour)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    
    # 'Crop' 1
    stencil = np.zeros(image.shape).astype(image.dtype) # Bit trick
    color = [255, 255, 255]
    cv2.fillPoly(stencil, [box], color)
    l1_result = cv2.bitwise_and(image, stencil)

    # -- Layer 2 --
    
    # Less-intense blur (TODO: remove hard-coded kernel values)
    blurred2 = cv2.GaussianBlur(l1_result, (51, 51), 0)
    gray2 = cv2.cvtColor(blurred2, cv2.COLOR_BGR2GRAY)
    pixels = []
    for i in range(gray2.shape[0]):
        for j in range(gray2.shape[1]):
            if gray2[i,j] > 20: # Mitigate border effect 
                pixels.append(gray2[i,j])
    mcp = st.mode(pixels)
    delta = mcp*0.05 # Neighborhood about the most colorful (TODO: make this an actual statistical variance measure)
    thresh2 = cv2.threshold(gray2, (mcp-delta), (mcp+delta), cv2.THRESH_BINARY)[1]
    f_contour = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0][0]
    
    # L2 Rectangle
    rect2 = cv2.minAreaRect(f_contour)
    box2 = cv2.boxPoints(rect2)
    box2 = np.int0(box2)
    cv2.drawContours(image,[box2],0,(0,0,255),3)

    # 'Crop' 2
    stencil2 = np.ones(image.shape).astype(image.dtype) # Bit trick (but in reverse to compensate for the first one)
    cv2.fillPoly(stencil2, [box2], color)
    l2_result = cv2.bitwise_and(image, stencil2)

    cv2.imshow('Original', image)
    cv2.imshow('Result', l2_result)
 
# For real-time video input (needs work)
def live():
    cap = cv2.VideoCapture(0)
    while True:
        _, frame = cap.read()
        cv2.imshow("Input Stream", frame)
        crop(frame)
        key = cv2.waitKey(1)
        if key == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

    return 0


