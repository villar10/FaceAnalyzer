"""=============
    Example : face_box.py
    Author  : Saifeddine ALOUI
    Description :
        A code to test FaceAnalyzer detects a face, draws a mask around it and measure head position and orientation
<================"""
from FaceAnalyzer import FaceAnalyzer, Face,  DrawingSpec
import numpy as np
import cv2
import time

# open camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Build face analyzer while specifying that we want to extract just a single face
fa = FaceAnalyzer(max_nb_faces=1)

# FPS processing
prev_frame_time = time.time()
curr_frame_time = time.time()

# Main Loop
while cap.isOpened():
    # Read image
    success, image = cap.read()
    
    # Opencv uses BGR format while mediapipe uses RGB format. So we need to convert it to RGB before processing the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to extract faces and draw the masks on the face in the image
    fa.process(image)

    if fa.nb_faces>0:
        face = fa.faces[0]
        # Get head position and orientation compared to the reference pose (here the first frame will define the orientation 0,0,0)
        pos, ori = face.get_head_posture(orientation_style=0)

        face.draw_bounding_box(image, thickness=5)
        face.draw_contour(image, face.getlandmarks_pos(Face.face_orientation_landmarks))
        #face.draw_landmark()
        eye_pos = face.getlandmark_pos(Face.left_eye_center_index)
        vector= ori.T @ np.array([100,0,0])
        vector = eye_pos+vector
        cv2.line(image, (int(eye_pos[0]),int(eye_pos[1])), (int(vector[0]),int(vector[1])), (255,0,0),1)
        vector= ori.T @ np.array([0,100,0])
        vector = eye_pos+vector
        cv2.line(image, (int(eye_pos[0]),int(eye_pos[1])), (int(vector[0]),int(vector[1])), (0,255,0),1)
        vector= ori.T @ np.array([0,0,100])
        vector = eye_pos+vector
        cv2.line(image, (int(eye_pos[0]),int(eye_pos[1])), (int(vector[0]),int(vector[1])), (0,0,255),1)
        # Show 
        ori = Face.rotationMatrixToEulerAngles(ori)
        cv2.putText(
            image, f"Yaw : {ori[1]*180/np.pi:2.0f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
        cv2.putText(
            image, f"Pitch : {ori[0]*180/np.pi:2.0f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.putText(
            image, f"Roll : {ori[2]*180/np.pi:2.0f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        cv2.putText(
            image, f"Position : {pos[0]:2.2f},{pos[1]:2.2f},{pos[2]:2.2f}", (10, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

    # Process fps
    curr_frame_time = time.time()
    dt = curr_frame_time-prev_frame_time
    prev_frame_time = curr_frame_time
    fps = 1/dt
    # Show FPS
    cv2.putText(
        image, f"FPS : {fps:2.2f}", (10, 150), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

    # Show the image
    try:
        cv2.imshow('Face Mesh', cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    except Exception as ex:
        print(ex)
    
    # Wait for key stroke for 5 ms
    wk = cv2.waitKey(5)
    if wk & 0xFF == 27: # If escape is pressed then return
        break

# Close the camera properly
cap.release()