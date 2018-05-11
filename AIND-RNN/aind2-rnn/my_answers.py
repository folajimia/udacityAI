import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
         
    # containers for input/output pairs
    X = []
    y = []
    for j in range(len(series)-window_size):
        X.append(series[0+j:window_size+j])
        y.append([(series[window_size+j])])
    
    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)
    
    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model =Sequential()
    model.add(LSTM(5, input_shape=(window_size,1)))
    model.add(Dense(1))
    #model.compile(loss='mean_squared_error', optimizer='adam')
    return (model)


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    unique_chars = set(text)
    punctuation = ['!', ',', '.', ':', ';', '?']
    allowed_letters = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
          'p','q','r','s','t','u','v','w','x','y','z'}
    unwanted = unique_chars - allowed_letters - set(punctuation)
    #cleaned = text.translate({ord(x): ' ' for x in unwanted})
    for x in unwanted:
        text = text.replace(x, ' ')
 
    return(text)





### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []   
    for j in range(0, len(text)-window_size,step_size):
        inputs.append(text[j:window_size+j])
        outputs.append((text[window_size+j]))
    
    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model =Sequential()
    model.add(LSTM(200, input_shape= (window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))
    
    return(model)
