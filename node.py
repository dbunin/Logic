"""
   

"""
class Tree:
    
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
    
    def __str__(self):
        return str(self.cargo)

    def addChild(self, tree):
        if self.left is None:
            self.left = tree
        elif self.right is None:
            self.right = tree
        else:
            raise ValueError

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def getResult(self, variables, values, node):
        if not self.checkIfSignIsCorrect(node.data):
            return values[variables.index(node.data)]
        else:
            leftValue = self.getResult(variables, values, node.left)
            rightValue = -1
            if node.right is not None:
                rightValue = self.getResult(variables, values, node.right)
            return self.executeSign(node.data, leftValue, rightValue)
            
    def executeSign(self, data, left, right):
        if data == '&':
            if left == '1' and right == '1':
                return '1'
            return '0'
        elif data == '|':
            if left == '1' or right == '1':
                return '1'
            return '0'
        elif data == '>':
            if left == '1' and right == '0':
                return '0'
            return '1'
        elif data == '~':
            if left == '1':
                return '0'
            return '1'
        else:
            if left == right:
                return '1'
            return '0'

    def checkIfSignIsCorrect(self, sign):
        possibleSigns = ['&', '|', '>', '~', '=']
        return sign in possibleSigns
