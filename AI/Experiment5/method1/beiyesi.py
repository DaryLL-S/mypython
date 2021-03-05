from collections import Counter
from matplotlib import pyplot as plt

from sklearn.preprocessing import LabelEncoder
import jieba
import numpy as np
import random
import pandas as pd
random.seed(2020)

# 数据集载入
data = pd.read_csv('Rumors01.csv')
data.head()

# 将rumorType转化成数字
truth_le = LabelEncoder()
new_rumor = truth_le.fit_transform(data['rumorType'])
data['rumorType'] = new_rumor

data['crawlTime'] = pd.to_datetime(data['crawlTime'])
data = data.sort_values(by='crawlTime')
# data.shape

rumor_gp = data.groupby(['crawlTime'])['title'].agg('count').reset_index()

fig,ax = plt.subplots(figsize=(16,9))
plt.plot(rumor_gp['crawlTime'],rumor_gp['title']);


rumor_ByType = data.groupby(['crawlTime','rumorType'])['title'].agg('count').reset_index()
# rumor_ByType
rumor_ByType = rumor_ByType.pivot(index='crawlTime',columns='rumorType',values='title')
rumor_ByType = rumor_ByType.rename_axis(None, axis=1)
# rumor_ByType
rumor_ByType = rumor_ByType.rename(columns = {1:'FAKE',2:'DOUBT',0:'TRUE'})
rumor_ByType = rumor_ByType.fillna(0)

fig,ax = plt.subplots(figsize=(16,9))
ax.plot_date(rumor_ByType.index,rumor_ByType['DOUBT'],fmt='g-')
ax.plot_date(rumor_ByType.index,rumor_ByType['TRUE'],fmt='b-')
ax.plot_date(rumor_ByType.index,rumor_ByType['FAKE'],fmt='r-')
plt.legend(['DOUBT','TRUE','FAKE'])
fig.autofmt_xdate()

from sklearn.metrics import *
y_dum = np.ones(len(data['rumorType'].values))
score1 = accuracy_score(y_dum, data['rumorType'])

from sklearn.feature_extraction.text import TfidfVectorizer
zhTokenizer = jieba.cut
v = TfidfVectorizer(token_pattern=r'(?u)\b\w+\b',
                    tokenizer = zhTokenizer,
                    lowercase = False,
                    stop_words = ['是','的'],
                    max_features = 250)

y = data['rumorType']
X_txt = data.drop(['rumorType','crawlTime','mainSummary'],axis=1)

from sklearn.model_selection import train_test_split,cross_val_score,cross_validate
X_tr,X_te,y_tr,y_te = train_test_split(X_txt,y,test_size=0.2,stratify=y)

#Convert X_train
X_tr_v = v.fit_transform(X_tr['title'])

from sklearn.naive_bayes import MultinomialNB as mnb
model_bl = mnb()
model_bl.fit(X_tr_v,y_tr.values)

X_te_v = v.transform(X_te['title'])
y_pred = model_bl.predict(X_te_v)

score2 = accuracy_score(y_pred,y_te)