#-*-coding:utf8 -*-
#导入mnist数据集
import numpy as np
import os, gzip
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#向量机
from sklearn.svm import SVC

#加载本地mnist数据集
def load_data(data_folder):

    files = [
        'train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
        't10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz'
    ]
    paths = []
    for fname in files:
        paths.append(os.path.join(data_folder,fname))

    with gzip.open(paths[0], 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[1], 'rb') as imgpath:
        x_train = np.frombuffer(
            imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28)

    with gzip.open(paths[2], 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)

    with gzip.open(paths[3], 'rb') as imgpath:
        x_test = np.frombuffer(
            imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28)

    return (x_train, y_train), (x_test, y_test)

print ("mnist data loaded")

(train_images, train_labels), (test_images, test_labels) = load_data('/data')
print ("original training data shape:",train_images.shape)
print ("original testing data shape:",test_images.shape)

#将每张图片展开到一维
train_data=train_images.reshape(60000,784)
test_data=test_images.reshape(10000,784)
print ("training data shape after reshape:",train_data.shape)
print ("testing data shape after reshape:",test_data.shape)

#利用主成分分析对数据进行降维
#提取了原有图片的100个主要特征，并构建了100维的特征空间
pca = PCA(n_components = 100)
pca.fit(train_data) #fit PCA with training data instead of the whole dataset
train_data_pca = pca.transform(train_data)
test_data_pca = pca.transform(test_data)
print("PCA completed with 100 components")
print ("training data shape after PCA:",train_data_pca.shape)
print ("testing data shape after PCA:",test_data_pca.shape)

#创建学习模型
print("正在创建学习模型")
svc = SVC(kernel = 'rbf')
svc.fit(train_data_pca,train_labels)
y_pre_svc = svc.predict(test_data_pca)
print("学习模型创建完成！")

#展示前100的测试样本数据
samples = test_images[:100]
y_pre = y_pre_svc[:100]

plt.figure(figsize=(12,18))
for i in range(100):
    plt.subplot(10,10,i+1)
    plt.imshow(samples[i].reshape(28,28),cmap='gray')
    title = 'True:'+str(test_labels[i])+'\nSVC:'+str(y_pre[i])
    plt.title(title)
    plt.axis('off')
plt.show()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(test_data_pca[:, 0], test_data_pca[:, 1], test_data_pca[:, 2], c=test_labels, cmap=plt.cm.Spectral)
plt.show()

print("前100个图像测试准确率：%.2f%%"%(svc.score(test_data_pca[:100],test_labels[:100])*100))
print("前1000个图像测试准确率：%.2f%%"%(svc.score(test_data_pca[:1000],test_labels[:1000])*100))
print("前10000个图像测试准确率：%.2f%%"%(svc.score(test_data_pca[:10000],test_labels[:10000])*100))