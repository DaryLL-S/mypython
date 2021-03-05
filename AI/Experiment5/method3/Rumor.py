import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# 读取数据
data = pd.read_csv('Rumors02.csv')

# 将数据按照“rumorType”进行分类
data['rumorType'] = data['rumorType'].map(lambda x: 0.0 if x == 'FAKE' else 1.0)
data.head()

# 将“title”和“mainSummary”分类下的内容合并为“content”
content	= data[['mainSummary','title']].apply(lambda x:' '.join(x),axis=1)
content.head()

# 原始文本转化为tf-idf的特征矩阵
from sklearn.feature_extraction.text import TfidfVectorizer as TFIDF
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split

# 对数据进行洗牌处理
from sklearn.utils import shuffle
X_shuf, Y_shuf = shuffle(content, data['rumorType'])

# 将有标签的数据集划分成训练集和测试集
train_X,test_X,train_y,test_y = train_test_split(X_shuf,Y_shuf,test_size=0.2,random_state=42)

# 模型构建
model_tfidf = TFIDF(min_df=5, max_features=5000, ngram_range=(1,3), use_idf=1, smooth_idf=1)
# 学习idf vector
model_tfidf.fit(train_X)
# 把文档转换成 X矩阵（该文档中该特征词出现的频次），行是文档个数，列是特征词的个数
train_vec = model_tfidf.transform(train_X)

# 模型训练
model_SVC = LinearSVC()
clf = CalibratedClassifierCV(model_SVC)
clf.fit(train_vec,train_y)

# 把文档转换成矩阵
test_vec = model_tfidf.transform(test_X)
# 验证
pre_test = clf.predict_proba(test_vec)
var = pre_test[:5]

from sklearn.metrics import accuracy_score

pre_test = clf.predict(test_vec)
score = accuracy_score(pre_test,test_y)
print("准确率:",score)