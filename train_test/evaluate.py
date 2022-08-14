from keras import models, optimizers
from keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from matplotlib import pyplot as plt
import numpy as np

model = models.load_model(r'C:\Users\shepherdm\Documents\school\deep learning\final project\CNN_RPS\model.h5')

model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.Adam(),
    metrics=['accuracy']
)

base_dir = 'dataset'

val_data = ImageDataGenerator(validation_split=0.2).flow_from_directory(
    base_dir,
    target_size=(200,300),
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    color_mode="grayscale"
    )

predictions = model.predict(val_data)
predictions = np.argmax(predictions, axis=1)
print('Confusion Matrix')
confusion_matrix = confusion_matrix(val_data.classes, predictions)
print(confusion_matrix)

print("Classification Report")
target_names = ['paper', 'rock', 'scissors']
print(classification_report(val_data.classes, predictions, target_names=target_names))
confMat = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix, display_labels=target_names)
confMat.plot(cmap=plt.cm.Blues)
#plt.show()
plt.savefig("confusion_matrix.png")
