from flask import Flask, render_template, request
import cv2
from keras.models import load_model
from numpy import expand_dims, frombuffer, array, uint8
from base64 import b64decode
import mediapipe as mp
from random import choice

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.1)
mp_drawing = mp.solutions.drawing_utils

model = load_model('model.h5')

# instatiate flask app
app = Flask(__name__, template_folder='./templates')


# convert image to keras friendly, predict class
def predict(img):
    classes = model.predict(img, batch_size=10)[0]
    if classes[0] > classes[1] and classes[0] > classes[2]:
        result = "paper"
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        result = "rock"
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        result = "scissors"
    return result


# decide winner based on predicted class and random cpu choice
def decide_winner(player_choice):
    cpu_choice = choice(['rock', 'paper', 'scissors'])
    if player_choice == cpu_choice:
        return [player_choice, cpu_choice, "tied"]
    elif player_choice == "scissors" and cpu_choice == "rock":
        return [player_choice, cpu_choice, "lost"]
    elif player_choice == "rock" and cpu_choice == "paper":
        return [player_choice, cpu_choice, "lost"]
    elif player_choice == "paper" and cpu_choice == "scissors":
        return [player_choice, cpu_choice, "lost"]
    else:
        return [player_choice, cpu_choice, "won"]


# serve the webpage
@app.route('/')
def index():
    return render_template("index.html")


# recieve and respond when image is sent from client side
@app.route('/get_image', methods=['POST', 'GET'])
def get_image():
    image_encoded = request.values['imageBase64']
    img_bytes = b64decode(image_encoded)
    img_arr = frombuffer(img_bytes, dtype=uint8)
    img = cv2.imdecode(img_arr, flags=cv2.IMREAD_COLOR)  # change to grayscale if wanted
    img = cv2.cvtColor(array(img), cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (300, 200), interpolation=cv2.INTER_AREA)
    hand_detect = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if hand_detect.multi_hand_landmarks:
        img[:, :, ] = 0
        for hand_no, hand_landmarks in enumerate(hand_detect.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image=img, landmark_list=hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = expand_dims(img, axis=0)
        condition = decide_winner(predict(img))
        return "You chose " + condition[0] + " and the computer chose " + condition[1] + " so you " + condition[2] + "."
    else:
        return "No hand detected."


if __name__ == '__main__':
    app.run(host='0.0.0.0')
