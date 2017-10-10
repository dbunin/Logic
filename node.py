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
        elif data == '%':
            if left == '1' and right == '1':
                return '0'
            return '1'
        else:
            if left == right:
                return '1'
            return '0'

    def checkIfSignIsCorrect(self, sign):
        possibleSigns = ['&', '|', '>', '~', '=']
        return sign in possibleSigns

    def findSigns(self):
        array = []
        if self.right is not None:
            array.extend(self.findSigns(self.right))
        if self.left is not None:
            array.extend(self.findSigns(self.left))
        if self.checkIfSignIsCorrect(self.data):
            array.append(self)
        return array
        
    def findVariables(self):
        array = []
        if self.checkIfSignIsCorrect(self.data) is False:
            array.append(self.data)
            return list(set(array))
        else:
            if self.right is not None:
                array.extend(self.findVariables(self.right))
            if self.left is not None:
                array.extend(self.findVariables(self.left))
            return list(set(array))

    def nanDify(self, node):
        if node.data == '&':
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            node.left = left_child
            node.right = right_child
            return node
        elif node.data == '|':
            newNode = Tree('%')
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            newNode.left = Tree('~')
            newNode.left.addChild(left_child)
            newNode.right = Tree('~')
            newNode.right = right_child
            return newNode
        elif node.data == '>':
            newNode = Tree('%')
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            newNode.left = left_child
            newNode.right = Tree('~')
            newNode.right = right_child
            return newNode
        elif node.data == '~':
            left_child = self.nanDify(node.right)
            node.left = left_child
            return node
        elif node.data == '=':
            newNode = Tree('%')
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            newNode.left = Tree('%')
            newNode.left.addChild(Tree('~'))
            newNode.left.left.addChild(left_child)
            newNode.left.right.addChild(right_child)
            newNode.right = Tree('%')
            newNode.right.addChild(left_child)
            newNode.right.addChild(right_child)
            return newNode
        else:
            return node
