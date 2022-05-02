# -*- coding: utf-8 -*-
"""DistanceLineProtectionZone-DeepNeuralNetwork.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1akwQJDo2d4iXak-gpp4v7qlcad9W5DbP
"""

!pip3 install ann_visualizer
!pip3 install keras-visualizer

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import tensorflow as tf

from keras.regularizers import l2
from keras.models import Sequential
from keras.layers import Dense

from sklearn.metrics import accuracy_score

from ann_visualizer.visualize import ann_viz
from keras_visualizer import visualizer

from google.colab import files
uploaded = files.upload()

datasets = pd.read_csv('DistanceDataset.csv', sep=',')
X = datasets.iloc[:, [0,1]].values
Y = datasets.iloc[:, 2].values
datasets.head()

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 0.25, random_state = 0)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_Train)

X_train1 = scaler.transform(X_Train)
X_train1 = X_train1.astype(np.float32)

X_test1 = scaler.transform(X_Test)
X_test1 = X_test1.astype(np.float32)

n = 0
for item in Y_Train:
  if item == 1.03:
    Y_Train[n] = 1
  elif item == 0:
    Y_Train[n] = 0
  elif item == 0.23:
    Y_Train[n] = 2
  elif item == 0.43:
    Y_Train[n] = 3
  else:
    Y_Train[n] = 4
  n += 1
Y_Train

n = 0
for item in Y_Test:
  if item == 1.03:
    Y_Test[n] = 1
  elif item == 0:
    Y_Test[n] = 0
  elif item == 0.23:
    Y_Test[n] = 2
  elif item == 0.43:
    Y_Test[n] = 3
  else:
    Y_Test[n] = 4
  n += 1
Y_Test

model = Sequential()
model.add(Dense(10, input_dim=2, activation='relu', kernel_regularizer=l2(0.2)))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(10, activation = 'relu'))
model.add(Dense(8, activation = 'relu'))
model.add(Dense(5, activation = 'softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary() 

history = model.fit(X_train1, Y_Train, validation_data = (X_test1, Y_Test), epochs=500, verbose=2)

ann_viz(model, title="Distance_Protection_Curve_DeepNeuralNetwork");
visual = visualizer(model, format='png', view=True)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

all_predict = model.predict(X_test1)
# print(all_predict)
all_pred_main = []
n = 0
for r in all_predict:
  if find_nearest(all_predict[n], 1)[1] == 0:
    all_pred_main.append(0)
  elif find_nearest(all_predict[n], 1)[1] == 1:
    all_pred_main.append(1)
  elif find_nearest(all_predict[n], 1)[1] == 2:
    all_pred_main.append(2)
  elif find_nearest(all_predict[n], 1)[1] == 3:
    all_pred_main.append(3)
  elif find_nearest(all_predict[n], 1)[1] == 4:
    all_pred_main.append(4)
  n = n+1
print(Y_Test)
print(all_pred_main)
print("accuracy deep neural network: ", accuracy_score(Y_Test, all_pred_main))

# summarize history for accuracy
figure(figsize=(15, 10), dpi=80)
fig1 = plt.gcf()

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

fig1.savefig("model_accuracy.png", dpi=200)
files.download("model_accuracy.png")

figure(figsize=(15, 10), dpi=80)
fig1 = plt.gcf()

plt.plot(history.history['loss']) 
plt.plot(history.history['val_loss']) 
plt.title('Model loss') 
plt.ylabel('Loss') 
plt.xlabel('Epoch') 
plt.legend(['Train', 'Test'], loc='upper left') 
plt.show()
plt.draw()

fig1.savefig("dnn_resolve_overfitting.png", dpi=200)
files.download("dnn_resolve_overfitting.png")

all_predict = model.predict(X_test1)
print(Y_Test)
all_predict

x_sample = scaler.transform([[-12, -1]])
x_sample = scaler.transform([[14, -1]])
x_sample = scaler.transform([[10, -5]])
x_sample = scaler.transform([[6, -2.5]])

x_sample = x_sample.astype(np.float32)

predict = model.predict(x_sample)
print(predict)
print()
print(find_nearest(predict[0], 1))
print()
if find_nearest(predict[0], 1)[1] == 0:
  print("Result: " + str(0))
elif find_nearest(predict[0], 1)[1] == 1:
  print("Result: " + str(1.03))
elif find_nearest(predict[0], 1)[1] == 2:
  print("Result: " + str(0.23))
elif find_nearest(predict[0], 1)[1] == 3:
  print("Result: " + str(0.43))
elif find_nearest(predict[0], 1)[1] == 4:
  print("Result: " + str(0.03))

model.save( 'models/model.h5' )

tflite_model = tf.keras.models.load_model('models/model.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(tflite_model)
tflite_save = converter.convert()
open("tfliteModel.tflite", "wb").write(tflite_save)