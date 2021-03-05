#=================2018093054====================#
# -*- coding:utf-8 -*-
import xlrd
import numpy as np
from numpy.linalg import eig
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

#===================读取数据======================#
fname = '各省经济指标.xlsx'
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("Sheet1")
except:
    print('no sheet in %s named Sheet1',format(fname))

nrows = sh.nrows
ncols = sh.ncols

cell_value = sh.cell_value(1,1)

row_list = []
for i in range(2,nrows):
    row_data = sh.row_values(i)
    row_list.append(row_data)

data_list = []
for i in range(0, len(row_list)):
    data_list.append(row_list[i][2:11])

#==================MyPCA=======================#
#=================2018093054===================#
data = np.array(data_list)
n,d = data.shape# n为样本个数，d为样本维数

mean = data.mean(axis=0) # 样本均值
M_data = data - mean # 通过去除平均值进行标准化,得到去中心化数据M_data
S_data = np.cov(M_data.T,ddof=0) # 计算去中心化数据M_data的协方差矩阵
eigenvalues, eigenvectors = eig(S_data) # 计算协方差矩阵S_data的特征值和特征向量

# 确定有多少个特征向量作为评价标准
t = 0
for t in range(0,n):
    value = sum(eigenvalues[0:t])/sum(eigenvalues[0:n])
    if value > 0.997:
        break
print('学号：2018093054')
print('t=%d'%(t))
# 根据贡献率得出排名前t个的特征向量
eig_pairs = [(np.abs(eigenvalues[i]), eigenvectors[:,i]) for i in range(d)]
eig_pairs.sort(reverse=True)
feature = np.array([ele[1] for ele in eig_pairs[:t]])

Mypca_data = np.dot(-M_data, feature.T) # M_data和k个特征向量点乘
print(Mypca_data) # 输出降维结果

tot = sum(eigenvalues)   # 计算特征值的和
var_exp = [(i / tot) for i in sorted(eigenvalues,reverse=True)] # 按照降序排列特征值，并计算贡献率
cum_var_exp = np.cumsum(var_exp)  #累计贡献度
plt.bar(range(1,len(var_exp)+1),var_exp,alpha=0.5,align='center',label='individual var') # 绘制柱状图
plt.step(range(1,len(var_exp)+1),cum_var_exp,where='mid',label='cumulative var')   # 绘制阶梯图
plt.ylabel('variance rtion')       # 纵坐标
plt.xlabel('principal components') # 横坐标
plt.legend(loc='best')  # 图例位置，右下角
plt.show()

#=====================sklearn-PCA========================#
#======================2018093054========================#
pca_data = PCA(n_components=t)
pca_data.fit(data)
New_data = pca_data.fit_transform(data)
print(" ")
print(New_data) # 输出降维结果
print(pca_data.explained_variance_ratio_)  # 输出贡献率

#======================经济实力排名========================#
#======================2018093054========================#
Range_data = Mypca_data.sum(axis=1)
Range_loc = np.argsort(-Range_data)
for i in range(0,Range_loc.size):
    print("第%d名:"%(i+1),row_list[Range_loc[i]][1])
