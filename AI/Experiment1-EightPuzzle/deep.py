Matrix_goal = [1,2,3,
               4,5,6,
               7,8,0]

class Tree:
    def __init__(self,rootObj):
        self.key = rootObj
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.father = None

    def insertUp(self,newNode):
        if self.up == None:
            self.up = Tree(newNode)
            self.up.father = self
        else:
            t = Tree(newNode)
            t.father = self
            self.up.father = t
            t.up = self.up
            self.up = t

    def insertDown(self,newNode):
        if self.down == None:
            self.down= Tree(newNode)
            self.down.father = self
        else:
            t = Tree(newNode)
            t.father = self
            self.down.father = t
            t.down = self.down
            self.down = t

    def insertLeft(self,newNode):
        if self.left == None:
            self.left = Tree(newNode)
            self.left.father = self
        else:
            t = Tree(newNode)
            t.father = self
            self.left.father = t
            t.left = self.left
            self.left = t

    def insertRight(self,newNode):
        if self.right == None:
            self.right = Tree(newNode)
            self.right.father = self
        else:
            t = Tree(newNode)
            t.father = self
            self.right.father = t
            t.right = self.right
            self.right = t

    def getUp(self):
        return self.up
    def getDown(self):
        return self.up
    def getLeft(self):
        return self.up
    def getRight(self):
        return self.up
    def getFather(self):
        return self.father
    def getRoot(self):
        return self.key
    def setRoot(self,obj):
        self.key = obj

def myNode(root):
    return []