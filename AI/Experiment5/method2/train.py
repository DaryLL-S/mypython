
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

data2 = pd.read_csv(r'train.csv')

for i in data2.columns:
    print('%s的分布:\n' % i, data2[i].value_counts())
    print('---------------------')


sns.countplot(data2['rumorType'])
plt.show()

labels = []
for i in range(len(data2['rumorType'])):
    if data2['rumorType'][i] == 'FAKE':
        labels.append(1)
    if data2['rumorType'][i] == 'TRUE':
        labels.append(0)
    if data2['rumorType'][i] == 'DOUBT':
        labels.append(2)
        
        
train = data2['content']
train.head()

import string
import jieba
import re
import tensorflow as tf
import sklearn as sl

def tokenize_text(text):
    tokens = jieba.cut(text, cut_all=False)
    tokens = [token.strip() for token in tokens]
    return tokens

def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text

def normalize_corpus(corpus, tokenize=False):
    normalized_corpus = []
    for text in corpus:
        text = remove_special_characters(text)
        text = remove_stopwords(text)
        normalized_corpus.append(text)
        if tokenize:
            text = tokenized_corpus.append(text)
    return normalized_corpus
    
with open(r'stopwords.txt') as f:
    stopwords = f.read()

norm_corpus = normalize_corpus(train)

b = []
c = 0
for i in norm_corpus:
    a = len(i)
    b.append(a)
    c += a

fig = plt.figure(figsize=(15, 4))
sns.countplot(b)
print('词数：', c)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vec = TfidfVectorizer(analyzer='word', max_features=40000, ngram_range=(1, 4),
                            binary=True, use_idf=1, smooth_idf=1, sublinear_tf=1, norm='l2').fit_transform(norm_corpus)

labels = np.array(labels)

labels = np.array(labels)

from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(tfidf_vec, labels, test_size=.2, shuffle=True, random_state=42)

a = train_x.toarray()
print('a:', a.shape)

b = test_x.toarray()
print('b:', b.shape)

train_xx = np.reshape(a, (39928, 1,40000))
test_xx= np.reshape(b, ((9982,1, 40000)))

model_k = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(36, return_sequences=True),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.GRU(24, return_sequences=True),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.SimpleRNN(12, return_sequences=True),
    tf.keras.layers.Dropout(0.1),
    tf.keras.layers.Dense(3, activation='softmax')
])

model_k.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])


import os
checkpoint_save_path = '2.ckpt'
if os.path.exists(checkpoint_save_path + '.index'):
    print('-----load model---------')
    model_k.load_weights(checkpoint_save_path)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                 save_weights_only=True,
                                                 asve_best_only=True, monitor='val_loss')

history = model_k.fit(train_xx, train_y, batch_size=32, epochs=100, callbacks=[cp_callback],
validation_data=(test_xx, test_y), validation_freq=1,)

model_k.summary()

from sklearn.metrics import accuracy_score
pre_y = model.predict_classes(test_xx)
acc = accuracy_score(test_y, pre_y)

print(acc)
