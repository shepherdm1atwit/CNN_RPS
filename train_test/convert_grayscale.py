import cv2
import mediapipe as mp
from os import listdir
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.1)
mp_drawing = mp.solutions.drawing_utils

for i in listdir(r'hands_dataset'):
    for j in listdir(r'hands_dataset/'+i):
        print(i+'/'+j)
        img = cv2.resize(cv2.imread('hands_dataset/'+i+'/'+j), (300,200), interpolation = cv2.INTER_AREA)
        results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            img[:, :, ] = 0
            for hand_no, hand_landmarks in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image=img, landmark_list=hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print(np.shape(img))
            quit()
            cv2.imwrite('dataset/'+i+'/'+j, img)