import cv2
from keras.models import load_model
from numpy import array, expand_dims, vstack, shape
import mediapipe as mp


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.1)
mp_drawing = mp.solutions.drawing_utils

model = load_model('../model.h5')
cam = cv2.VideoCapture(0)
runs_per = 0
inp = ""

while True:
    runs_per = int(input("How many times would you like to run each test? "))
    if runs_per <= 0:
        print("Please enter a number greater than 0")
    elif runs_per == "q":
        print("Ok bye then")
        quit()
    else:
        break

correct = {
    "rock": 0,
    "paper": 0,
    "scissors": 0
}
incorrect = {
    "rock-paper": 0,
    "rock-scissors": 0,
    "paper-rock": 0,
    "paper-scissors": 0,
    "scissors-rock": 0,
    "scissors-paper": 0
}


def predict():
    trash, img_source = cam.read()
    img_source = array(img_source)
    img_source = vstack([img_source])
    img_source = cv2.resize(img_source, (300, 200))
    handDetect = hands.process(cv2.cvtColor(img_source, cv2.COLOR_BGR2RGB))
    if handDetect.multi_hand_landmarks:
        img_source[:, :, ] = 0
        for hand_no, hand_landmarks in enumerate(handDetect.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image=img_source, landmark_list=hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)
        img_source = cv2.cvtColor(img_source, cv2.COLOR_BGR2GRAY)


    img_source = img_source / 255
    print(shape(img_source))
    img = expand_dims(img_source, axis=0)
    classes = model.predict(img, batch_size=10)[0]

    if classes[0] > classes[1] and classes[0] > classes[2]:
        return "paper"
    elif classes[1] > classes[0] and classes[1] > classes[2]:
        return "rock"
    elif classes[2] > classes[0] and classes[2] > classes[1]:
        return "scissors"


print("--------------------\n    ROCK TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up rock and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        correct["rock"] += 1
    elif prediction == "paper":
        incorrect["rock-paper"] += 1
    elif predict() == "scissors":
        incorrect["rock-scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    PAPER TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up paper and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        incorrect["paper-rock"] += 1
    elif prediction == "paper":
        correct["paper"] += 1
    elif predict() == "scissors":
        incorrect["paper-scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    SCISSORS TESTING\n--------------------")
for i in range(runs_per):
    if input("hold up scissors and press enter:") == "q":
        print("Ok bye then")
        quit()
    prediction = predict()
    if prediction == "rock":
        incorrect["scissors-rock"] += 1
    elif prediction == "paper":
        incorrect["scissors-paper"] += 1
    elif predict() == "scissors":
        correct["scissors"] += 1
    print("test number ", i + 1, " gave result: ", prediction)

print("--------------------\n    FINAL RESULTS\n--------------------")
print("The machine guessed the following signs correctly:\nRock: ",
      correct["rock"], "\nPaper: ", correct["paper"], "\nScissors: ", correct["scissors"])

print("Of the signs guessed incorrectly, the machine classified:\n", incorrect["rock-paper"], " rock as paper\n",
      incorrect["rock-scissors"], " rock as scissors\n", incorrect["paper-rock"], " paper as rock\n",
      incorrect["paper-scissors"], " paper as scissors\n", incorrect["scissors-paper"], " scissors as paper\n",
      incorrect["scissors-rock"], " scissors as rock\n")

rock_accuracy = (correct["rock"] / runs_per)*100
paper_accuracy = (correct["paper"] / runs_per)*100
scissors_accuracy = (correct["scissors"] / runs_per)*100
print("This results in accuracies of ", str(rock_accuracy), "% for rock ", str(paper_accuracy), "% for for paper, and ",
      str(scissors_accuracy), "% for scissors.\nOverall, this gives the machine a real world accuracy of ",
      str((rock_accuracy + paper_accuracy + scissors_accuracy) / (runs_per * 3)), "%")
