# -*- coding: utf-8 -*-
"""
Created on %(date)s

@author: %(username)s
"""

from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku 

# set seeds for reproducability

from numpy.random import seed
from tensorflow import random
random.set_seed(1)
seed(1)

import pandas as pd
import numpy as np
import string, os 

import warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

curr_dir = r"C:\Users\swetha\Downloads\project\text generation"
file_prefix = 'Articles'
file_extension = 'csv'
all_headlines = []
for filename in os.listdir(curr_dir):
    if 'Articles' in filename and filename.endswith('.csv'):
        file_path = os.path.join(curr_dir, filename)
        article_df = pd.read_csv(file_path)
        all_headlines.extend(list(article_df.headline.values))
        break



all_headlines = [h for h in all_headlines if h != "Unknown"]
len(all_headlines)

def clean_text(txt):
    txt = "".join(v for v in txt if v not in string.punctuation).lower()
    txt = txt.encode("utf8").decode("ascii",'ignore')
    return txt 

corpus = [clean_text(x) for x in all_headlines]
corpus[:10]


tokenizer = Tokenizer()

def get_sequence_of_tokens(corpus):
    ## tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    
    ## convert data to sequence of tokens 
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words

inp_sequences, total_words = get_sequence_of_tokens(corpus)

from keras.utils import np_utils

def generate_padded_sequences(input_sequences):
    if not input_sequences:
        # Return default values if input_sequences is empty
        return np.array([]), np.array([]), 0

    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    
    predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
    label = np_utils.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len

predictors, label, max_sequence_len = generate_padded_sequences(inp_sequences)


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()
    
    # Add Input Embedding Layer
    model.add(Embedding(total_words, 10))
    
    # Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))
    
    # Add Output Layer
    model.add(Dense(total_words, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam',run_eagerly=True)
    
    return model

model = create_model(max_sequence_len, total_words)
model.summary()


model.fit(predictors, label, epochs=500, verbose=5)


model.save(r'C:\Users\swetha\Downloads\project/newweight.h5')








