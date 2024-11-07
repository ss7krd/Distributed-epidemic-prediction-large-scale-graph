from __future__ import print_function
# import IPython
import sys
import tensorflow as tf
import numpy as np
# from keras import layers
from keras.layers import Permute, Lambda, Input, Add, RNN, Layer, LSTM, Reshape, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D, Conv1D, AveragePooling1D, AveragePooling2D, MaxPooling1D, MaxPooling2D, GlobalMaxPooling1D, GlobalMaxPooling2D, GlobalAveragePooling1D, GlobalAveragePooling2D, Dropout, Concatenate, concatenate
from keras.models import Model, load_model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.callbacks import ModelCheckpoint
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
from keras.losses import categorical_crossentropy as logloss
from keras.metrics import categorical_accuracy
# import pydot

np.random.seed(2017)

# from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model, to_categorical
from keras.initializers import glorot_uniform, he_uniform
import scipy.misc 
from matplotlib.pyplot import imshow

from keras import activations
from keras import initializers
from keras import regularizers
from keras import constraints

# from utils.generic_utils import load_dataset_at
# from utils.keras_modified_utils import LSTMCell_modified, LSTM_modified

import os
import h5py
import math

from keras.legacy.layers import Recurrent
from keras.legacy import interfaces

import keras.backend as K 
import pandas as pd

parentFolderName = "/home/sudipta/Lab_Materials/covid-19/Code/Mobility prediction/"

def load_dataset_at(index, fold_index=None, normalize_timeseries=False) -> (np.array, np.array):
    # if verbose: print("Loading train / test dataset : ", TRAIN_FILES[index], TEST_FILES[index])

    if index == 1:
        # parentFilePath = "/home/sudipta/Lab_Materials/hybrid_dnn/Code_v1/Main_Codes/compression/harDatasetWeights/"
        x_train_path = parentFolderName + "X_train.npy"
        # x_train_shot_path = parentFilePath + "X_train-shot.npy"
        # x_train_combined_path = parentFilePath + "X_train-gaussian-shot.npy"
        y_train_path = parentFolderName + "X_train.npy"
        x_test_path =  parentFolderName + "X_train.npy"
        y_test_path =  parentFolderName + "X_train.npy"
        # nb_classes = 6

    elif index == 2:
        
        parentFilePath = "/home/sudipta/Lab_Materials/hybrid_dnn/Code_v1/Main_Codes/compression/hharDatasetWeights/"
        x_train_gaussian_path = parentFilePath + "X_train-gaussian.npy"
        # x_train_shot_path = parentFilePath + "X_train-shot.npy"
        # x_train_combined_path = parentFilePath + "X_train-gaussian-shot.npy"
        y_train_path = parentFilePath + "y_train.npy"
        x_test_path =  parentFilePath + "X_test.npy"
        y_test_path =  parentFilePath + "y_test.npy"
        nb_classes = 6

    elif index == 3:
        parentFilePath = "/home/sudipta/Lab_Materials/hybrid_dnn/Code_v1/Main_Codes/compression/airDatasetWeights/"
        x_train_gaussian_path = parentFilePath + "train_X_gaussian.npy"
        # x_train_shot_path = parentFilePath + "train_X_shot.npy"
        # x_train_combined_path = parentFilePath + "train_X_combined.npy"
        y_train_path = parentFilePath + "train_Y.npy"
        x_test_path =  parentFilePath + "test_X.npy"
        y_test_path =  parentFilePath + "test_Y.npy"
        nb_classes = 2
    # if os.path.exists(x_train_path):
    X_train = np.load(x_train_path)
    # X_train_shot = np.load(x_train_shot_path)
    # X_train_combined = np.load(x_train_combined_path)
    y_train = np.load(y_train_path)
    X_test = np.load(x_test_path)
    y_test = np.load(y_test_path)
    # elif os.path.exists(x_train_path[1:]):
    #     X_train = np.load(x_train_path[1:])
    #     y_train = np.load(y_train_path[1:])
    #     X_test = np.load(x_test_path[1:])
    #     y_test = np.load(y_test_path[1:])
    # else:
    #     # raise FileNotFoundError('File %s not found!' % (TRAIN_FILES[index]))
    #     print("File not found")

    is_timeseries = True

    

    # extract labels Y and normalize to [0 - (MAX - 1)] range
    # nb_classes = len(np.unique(y_train))
    # y_train = (y_train - y_train.min()) / (y_train.max() - y_train.min()) * (nb_classes - 1)

    if is_timeseries:
        # scale the values
        if normalize_timeseries:
            X_train_mean = X_train.mean()
            X_train_std = X_train.std()
            X_train = (X_train - X_train_mean) / (X_train_std + 1e-8)

    if is_timeseries:
        # scale the values
        if normalize_timeseries:
            y_train_mean = y_train.mean()
            y_train_std = y_train.std()
            y_train = (y_train - y_train_mean) / (y_train_std + 1e-8)

    # if verbose: print("Finished processing train dataset..")

    # extract labels Y and normalize to [0 - (MAX - 1)] range
    # nb_classes = len(np.unique(y_test))
    # y_test = (y_test - y_test.min()) / (y_test.max() - y_test.min()) * (nb_classes - 1)

    if is_timeseries:
        # scale the values
        if normalize_timeseries:
            X_test = (X_test - X_train_mean) / (X_train_std + 1e-8)

    if is_timeseries:
        # scale the values
        if normalize_timeseries:
            y_test = (y_test - y_train_mean) / (y_train_std + 1e-8)

    # if verbose:
    #     print("Finished loading test dataset..")
    #     print()
    #     print("Number of train samples : ", X_train.shape[0], "Number of test samples : ", X_test.shape[0])
    #     print("Number of classes : ", nb_classes)
    #     print("Sequence length : ", X_train.shape[-1])

    # return X_train_gaussian, X_train_shot, X_train_combined, y_train, X_test, y_test, is_timeseries, nb_classes
    return X_train, y_train, X_test, y_test, is_timeseries


dataset_id = 1
X_train, y_train, X_test, y_test, is_timeseries = load_dataset_at(dataset_id)
y_train = np.reshape(y_train, (y_train.shape[1], y_train.shape[0], y_train.shape[2]))
y_test = np.reshape(y_test, (y_test.shape[1], y_test.shape[0], y_test.shape[2]))
print("Y_train shape", y_train.shape)

n_a = 100
number_of_routes = 10
feature_per_timestep = number_of_routes
number_of_timesteps_considered = 10

reshapor = Reshape((1, feature_per_timestep))        
LSTM_cell = LSTM(n_a, return_state = True)        
densor = Dense(number_of_routes, activation='softmax')     

lambda_timestamp = 0
def preprocess(inp):
    global lambda_timestamp
    return inp[:,lambda_timestamp,:]

def model_interpreter_rnn_cnn(Tx, n_a, n_values, number_of_routes):
 
    X_rnn = Input(shape=(Tx, n_values))
    # X_cnn = Permute((2, 1))(X_rnn)
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    # cosn = 10
    a = a0
    c = c0
    # a_shortcut_list = []
    # c_shortcut_list = []
    global lambda_timestamp
    # rnn_time_profiling = 0
    outputs = []
    for t in range(Tx):

        lambda_timestamp = t
        x = Lambda(preprocess)(X_rnn)
        x = reshapor(x)
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        # summ_tensor_a = a
        # summ_tensor_c = c
        out = Dense(number_of_routes, kernel_initializer='he_uniform')(a)
        outputs.append(out)

        # i = t+1


        # a, _, c = LSTM_cell(x, initial_state=[summ_tensor_a, summ_tensor_c])
        # a_shortcut_list.append(a)
        # c_shortcut_list.append(c)

    model = Model(inputs=[X_rnn, a0, c0], outputs=outputs)
    
    return model

model = model_interpreter_rnn_cnn(Tx = number_of_timesteps_considered, n_a = n_a, n_values = feature_per_timestep, number_of_routes = number_of_routes)

opt = 'adam'

model.compile(optimizer=opt, loss='mean_squared_error', metrics=['mse'])
filepath="mobility_prediction.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

m = X_train.shape[0]
a0 = np.zeros((m, n_a))
c0 = np.zeros((m, n_a))

m = X_test.shape[0]
a0_test = np.zeros((m, n_a))
c0_test = np.zeros((m, n_a))


model.fit([X_train, a0, c0], y_train.tolist(), batch_size=128, nb_epoch=200, validation_data = ([X_test, a0_test, c0_test], y_test.tolist()), callbacks=callbacks_list,verbose=1)

# model = model_interpreter_rnn_cnn(Tx = number_of_timesteps_considered, n_a = 100, n_values = feature_per_timestep, number_of_routes = number_of_routes)
# model.load_weights("mobility_prediction.hdf5")
# # model.compile(optimizer=opt, loss='mean_squared_error', metrics=['mse'])
# print("Created model and loaded weights from file")


# preds = model.evaluate([X_test, a0_test, c0_test], y_test, batch_size = 128)

# print("Loss:",preds[0])
# print("MSE:",preds[1])

def inference_model_interpreter_rnn_cnn(Tx, n_a, n_values, number_of_routes):
 
    x0 = Input(shape=(1, n_values))
    # X_cnn = Permute((2, 1))(X_rnn)
    a0 = Input(shape=(n_a,), name='a0')
    c0 = Input(shape=(n_a,), name='c0')
    # cosn = 10
    x = x0
    a = a0
    c = c0
    # a_shortcut_list = []
    # c_shortcut_list = []
    global lambda_timestamp
    # rnn_time_profiling = 0
    outputs = []
    for t in range(Tx):

        # lambda_timestamp = t
        # x = Lambda(preprocess)(X_rnn)
        # x = reshapor(x)
        a, _, c = LSTM_cell(x, initial_state=[a, c])
        # summ_tensor_a = a
        # summ_tensor_c = c
        out = Dense(number_of_routes, kernel_initializer='he_uniform')(a)
        outputs.append(out)
        x = reshapor(out)

        # i = t+1


        # a, _, c = LSTM_cell(x, initial_state=[summ_tensor_a, summ_tensor_c])
        # a_shortcut_list.append(a)
        # c_shortcut_list.append(c)

    model = Model(inputs=[X, a0, c0], outputs=outputs)
    
    return model

def predict_and_sample():
    inference_model = inference_model_interpreter_rnn_cnn(Tx = number_of_timesteps_considered, n_a = n_a, n_values = feature_per_timestep, number_of_routes = number_of_routes)
    x_initializer = np.zeros((1, feature_per_timestep))
    a_initializer = np.zeros((1, n_a))
    c_initializer = np.zeros((1, n_a))
    pred = inference_model.predict([x_initializer, a_initializer, c_initializer])
    return pred

# pred = predict_and_sample()


