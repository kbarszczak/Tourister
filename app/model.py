import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pickle
import keras

from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing import sequence
from keras import layers

import tensorflow as tf

model_path = '../models/tc_model_2_1681463923_tt_1681463733.h5'
dictionary_path = '../data/small_dictionary_1680888160.pickle'
tokenizer_path = '../models/tokenizer_1681463733.pickle'
places_path = '../data/places_krakow_vectorized_1681469611.pickle'
maxlen = 500

class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, ff_act='relu', ff_reg=None, ff_d=0.25, mh_reg=None, mh_d=0.1, norm_eps=1e-6, **kwargs):
        # initialize super class
        super(TransformerBlock, self).__init__(**kwargs)
        
        # multi head attention
        self.att = layers.MultiHeadAttention(
            num_heads=num_heads, 
            key_dim=embed_dim,
            kernel_regularizer=mh_reg,
            dropout=mh_d
        )
        
        # feed forward network
        self.ffn = keras.Sequential([
            layers.Dense(ff_dim, activation=ff_act, kernel_regularizer=ff_reg), 
            layers.Dense(embed_dim, kernel_regularizer=ff_reg)
        ])
        
        # layer normalizations
        self.layernorm1 = layers.LayerNormalization(epsilon=norm_eps)
        self.layernorm2 = layers.LayerNormalization(epsilon=norm_eps)
        
        # dropout layers
        self.dropout1 = layers.Dropout(ff_d)
        self.dropout2 = layers.Dropout(ff_d)
        
        # remember for serialization
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.ff_dim = ff_dim
        self.ff_act=ff_act
        self.ff_reg=ff_reg
        self.ff_d=ff_d
        self.mh_reg=mh_reg
        self.mh_d=mh_d
        self.norm_eps=norm_eps
        
    def get_config(self):
        config = super().get_config()
        config.update({
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "ff_dim": self.ff_dim,
            "ff_act": self.ff_act,
            "ff_reg": self.ff_reg,
            "ff_d": self.ff_d,
            "mh_reg": self.mh_reg,
            "mh_d": self.mh_d,
            "norm_eps": self.norm_eps
        })
        return config

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

class TokenAndPositionEmbedding(layers.Layer):
    def __init__(self, maxlen, vocab_size, embed_dim, embed_reg=None, **kwargs):
        super(TokenAndPositionEmbedding, self).__init__(**kwargs)
        
        # embedding layers
        self.token_emb = layers.Embedding(
            input_dim=vocab_size,
            output_dim=embed_dim,
            embeddings_regularizer=embed_reg
        )
        self.pos_emb = layers.Embedding(
            input_dim=maxlen, 
            output_dim=embed_dim,
            embeddings_regularizer=embed_reg
        )
        
        # save for serialization
        self.maxlen = maxlen
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.embed_reg = embed_reg

    def call(self, x):
        maxlen = tf.shape(x)[-1]
        positions = tf.range(start=0, limit=maxlen, delta=1)
        positions = self.pos_emb(positions)
        x = self.token_emb(x)
        return x + positions
    
    def get_config(self):
        config = super().get_config()
        config.update({
            "maxlen": self.maxlen,
            "vocab_size": self.vocab_size,
            "embed_dim": self.embed_dim,
            "embed_reg": self.embed_reg
        })
        return config

def load(model_path, tokenizer_path, places_path, dictionary_path):
    with open(tokenizer_path, 'rb') as file:
        tokenizer = pickle.load(file)
        
    with open(places_path, 'rb') as file:
        places = pickle.load(file)
        
    with open(dictionary_path, 'rb') as file:
        dictionary = pickle.load(file)
        dictionary = {value: key for key, value in dictionary.items()}
        
    model = keras.models.load_model(
        filepath = model_path, 
        custom_objects = {
            "TokenAndPositionEmbedding": TokenAndPositionEmbedding,
            "TransformerBlock": TransformerBlock
        }
    )
    
    return model, tokenizer, places, dictionary

def calculate_vector(model, tokenizer, text):
    sequences = tokenizer.texts_to_sequences([text])
    x = pad_sequences(sequences, maxlen=maxlen)
    return model.predict(x, verbose=0)[0]

def mse(vector, place_vector):
    return np.square(vector - place_vector).mean()

def best_fit_weighted_avg(vector, place_vector, weights=[2, 1.5, 1.5, 1, 1]):
    best_categories = np.argsort(vector)[::-1][0:len(weights)]
    difference = np.abs(place_vector[best_categories] - vector[best_categories])
    return np.average(difference, weights=weights)

def sort_places(vector, places, difference_metric=mse):
    buffer = []
    for place in places:
        buffer.append((place, difference_metric(vector, place[10])))
        
    buffer.sort(key=lambda x: x[1])
    
    return zip(*buffer)

model, tokenizer, places, dictionary = load(model_path, tokenizer_path, places_path, dictionary_path)

def get_places(text):
    result = calculate_vector(model, tokenizer, text)
    places_sorted, distances = sort_places(result, places, difference_metric=mse)
    return places_sorted