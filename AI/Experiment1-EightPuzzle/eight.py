__author__ = '2018093054QJC'
import numpy as np

class State:
    def __init__(self, state, directionFlag=None, parent=None,depth = 1):
        self.state = state #定义一个3x3的数组存储状态
        self.direction = ['up', 'down', 'right', 'left'] #定义上、下、左、右操作集
        if directionFlag:
            self.direction.remove(directionFlag) # 记录可能的方向生成子集
        self.parent = parent
        self.symbol = ' ' #将‘ ’作为移动的标识符
        self.answer = np.array([[1, 2, 3], [8, State.symbol, 4], [7, 6, 5]])   # 设置最终状态
        self.depth = depth
        # 计算不在正确位置上的元素个数
        num = 0
        for i in range(len(state)):
            for j in range(len(state)):
                if self.state[i, j] != ' 'and self.state[i, j] != self.answer[i, j]:
                    num += 1
        self.cost = num + self.depth

    def getDirection(self):
        #返回操作状态
        return self.direction

    def showInfo(self):
        #将成功的查询过程打印出来
        for i in range(3):
            for j in range(3):
                print(self.state[i, j], end='  ')
            print("\n")
        print('->')
        return

    def getEmptyPos(self):   #得到标识符的位置
        postion = np.where(self.state == self.symbol)
        return postion

    def generateSubStates(self):
        if not self.direction:  #判断self.direction是否为None，若为None，返回一个空列表[]
            return []
        subStates = []
        boarder = len(self.state) - 1   #边界的最大值，此处为3-1=2
        row, col = self.getEmptyPos()   #得到标识符的位置
        if 'left' in self.direction and col > 0: #判断是否能够左移
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col-1]
            s[row, col-1] = temp[row, col]
            news = State(s, directionFlag='right', parent=self)
            subStates.append(news)

        if 'up' in self.direction and row > 0: #判断是否能够上移
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row-1, col]
            s[row-1, col] = temp[row, col]
            news = State(s, directionFlag='down', parent=self)
            subStates.append(news)

        if 'down' in self.direction and row < boarder: #判断是否能够下移
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row+1, col]
            s[row+1, col] = temp[row, col]
            news = State(s, directionFlag='up', parent=self)
            subStates.append(news)

        if self.direction.count('right') and col < boarder: #判断是否能够右移
            s = self.state.copy()
            temp = s.copy()
            s[row, col] = s[row, col+1]
            s[row, col+1] = temp[row, col]
            news = State(s, directionFlag='left', parent=self)
            subStates.append(news)

        return subStates

    # BFS广度优先解决方法
    def weight_solve(self):
        openTable = []  # 生成一个空的openTable表
        closeTable = [] # 生成一个空的closeTable表
        openTable.append(self)  # 在openTable里塞入一个初始的状态
        steps = 1
        # 开始循环
        while len(openTable) > 0:   # 当openTable不为空时
            n = openTable.pop(0)    # pop弹出openTable里第一个元素
            closeTable.append(n)    # append将元素塞进closeTable表尾
            subStates = n.generateSubStates()   #生成子状态列表
            path = []   # 定义path作为路径的储存
            for s in subStates:
                if (s.state == s.answer).all(): # 判断子状态中有无与最终状态相同的状态
                    while s.parent and s.parent != RootState: # 保证不回到根状态（原始状态）
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()  # 将path列表中的元素反向
                    return path, steps+1
            openTable.extend(subStates) # 在openTable列表末尾一次性追加subStates列表中的多个值（用新列表扩展原来的列表）
            steps += 1
        else:
            return None, None

    # FS广深度优先解决方法
    def deep_solve(self):
        openTable = []  # 生成一个空的openTable表
        closeTable = [] # 生成一个空的closeTable表
        openTable.append(self)  # 在openTable里塞入一个初始的状态
        steps = 1
        # 开始循环
        while len(openTable) > 0:   # 当openTable不为空时
            n = openTable.pop()    # pop弹出openTable里最后一个元素
            closeTable.append(n)    # append将元素塞进closeTable表尾
            subStates = n.generateSubStates()   #生成子状态列表
            path = []   # 定义path作为路径的储存
            for s in subStates:
                if (s.state == s.answer).all(): # 判断子状态中有无与最终状态相同的状态
                    while s.parent and s.parent != RootState: # 保证不回到根状态（原始状态）
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()  # 将path列表中的元素反向
                    return path, steps+1
            openTable.extend(subStates) # 在openTable列表末尾一次性追加subStates列表中的多个值（用新列表扩展原来的列表）
            steps += 1
        else:
            return None, None

    #A*算法
    def A_solve(self):
        openTable = []
        closeTable = []
        openTable.append(self)
        steps = 0
        while len(openTable) > 0:
            n = openTable.pop(0)
            closeTable.append(n)
            subStates = n.generateSubStates()
            path = []
            for s in subStates:
                if (s.state == s.answer).all():
                    while s.parent and s.parent != RootState:
                        path.append(s.parent)
                        s = s.parent
                    path.reverse()
                    return path, steps+1
            openTable.extend(subStates)
            openTable.sort(key=lambda x: x.cost)
            steps += 1
        else:
            return None, None

if __name__ == '__main__':
    symbolFlag = ' '    # symbolflag表示要移动的点
    State.symbol = symbolFlag
    RootState = State(np.array([[2, 8, 3], [1, 6 , 4], [7, symbolFlag, 5]]))  # 设置初始状态
    s1 = State(state=RootState.state)
    n = int(input("请输入一个整数"))
    i = 0
    for i in range(0,n):
        commands = str(input("请输入一个操作(weight_solve/deep_solve/A_solve)"))
        if commands == 'weight_solve':
            path, steps = s1.weight_solve()
            if path:    # 如果此问题有解
                for node in path:    # 将每一步节点状态打印出来
                   node.showInfo()
                print(RootState.answer)
                print("总步数为 %d" % steps)

        if commands == 'deep_solve':
            path, steps = s1.deep_solve()
            if path:    # 如果此问题有解
                for node in path:    # 将每一步节点状态打印出来
                    node.showInfo()
                print(RootState.answer)
                print("总步数为 %d" % steps)

        if commands == 'A_solve':
            path, steps = s1.A_solve()
            if path:    # 如果此问题有解
                for node in path:    # 将每一步节点状态打印出来
                    node.showInfo()
                print(RootState.answer)
                print("总步数为 %d" % steps)