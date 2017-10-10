

class Tree:
    """
    Tree data structure.

    Args:
        data (str): the value of a node
        left (Tree): left child
        right (Tree): right child.

    Attributes:
        data (str): the value of a node
        left (Tree): left child
        right (Tree): right child.
    """
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
    
    def __str__(self):
        """
        Change to default toString.

        Attributes:
            other (Tree): The object self is comparing to.

        Returns:
            String: The value of a node.
        """
        return str(self.data)

    def __eq__(self, other):
        """
        Change to default comparing to the Object.

        Attributes:
            other (Tree): The object self is comparing to.

        Returns:
            Bool: The return value. True if objects are equal, False otherwise.
        """
        return self.__dict__ == other.__dict__

    def addChild(self, tree):
        """
        Add a child to the tree.

        Attributes:
            tree (Tree): The object to add as a child.

        Raises:
            ValueError if there are already two childs.
        """
        if self.left is None:
            self.left = tree
        elif self.right is None:
            self.right = tree
        else:
            raise ValueError

    def getResult(self, variables, values, node):
        """
        Get the boolean value of the whole tree and its subtrees.

        Attributes:
            variables (List): List of variables
            values    (List): List of values
            node      (Tree): Tree.

        Returns:
            String: The return value. '1' if True, '0' if False.
        """
        if not self.checkIfSignIsCorrect(node.data):
            return values[variables.index(node.data)]
        else:
            leftValue = self.getResult(variables, values, node.left)
            rightValue = -1
            if node.right is not None:
                rightValue = self.getResult(variables, values, node.right)
            return self.executeSign(node.data, leftValue, rightValue)
            
    def executeSign(self, data, left, right):
        """
        Executes a node.

        Attributes:
            data  (String): The value of a node
            left  (String): Value of a left subtree
            right (String): Value of a right subtree.

        Returns:
            String: The return value. '1' if True, '0' if False.
        """
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
        """
        Checks if the value of a node is a sign.

        Attributes:
            sign (String): The value of a node.

        Returns:
            Bool: The return value. True if the value of a node is a sign, False otherwise.
        """
        possibleSigns = ['&', '|', '>', '~', '=', '%']
        return sign in possibleSigns

    def findSigns(self):
        """
        Finds all signs in the tree.

        Returns:
            List: List with all the object of type Tree.
        """
        array = []
        if self.right is not None:
            array.extend(self.findSigns(self.right))
        if self.left is not None:
            array.extend(self.findSigns(self.left))
        if self.checkIfSignIsCorrect(self.data):
            array.append(self)
        return array
        
    def findVariables(self):
        """
        Finds all variables in the tree.

        Returns:
            List: List with all the variables of type String.
        """
        array = []
        if self.checkIfSignIsCorrect(self.data) is False:
            array.append(self.data)
            return list(set(array))
        else:
            if self.right is not None:
                array.extend(self.right.findVariables())
            if self.left is not None:
                array.extend(self.left.findVariables())
            return list(set(array))

    def nanDify(self, node):
        """
        Transforms a tree to a tree with only one type of sign `%`.

        Attributes:
            node (Tree): The tree object.

        Returns:
            Tree: Returns a root node.
        """
        if node is None:
            return
        if node.data == '&':
            tempTree = Tree('%')
            tempTree.addChild(Tree('%'))
            tempTree.addChild(Tree('%'))
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            tempTree.left.addChild(left_child)
            tempTree.left.addChild(right_child)
            tempTree.right.addChild(left_child)
            tempTree.right.addChild(right_child)
            return tempTree
        elif node.data == '|':
            newNode = Tree('%')
            left_child = self.nanDify(node.left)
            right_child = self.nanDify(node.right)
            newNode.left = Tree('%')
            newNode.left.addChild(left_child)
            newNode.left.addChild(left_child)
            newNode.right = Tree('%')
            newNode.right.addChild(right_child)
            newNode.right.addChild(right_child)
            return newNode
        elif node.data == '~':
            if(node.left.data == '~'):
                node = self.nanDify(node.left.left)
            else:
                left_child = self.nanDify(node.left)
                node = Tree('%')
                node.left = left_child
                node.right = left_child
            return node
        else:
            return node

    def clearDoubleNegation(self):
        """
        Deletes double negation from a tree
        """
        if self.data == '~':
            if self.left.data == '~':
                temp = self.left
                self.data = temp.left.data
                self.left = temp.left.left
                self.right = temp.left.right
        if self.left is not None:
            self.left.clearDoubleNegation()
        if self.right is not None:
            self.right.clearDoubleNegation()

    def getInfix(self):
        """
        Returns infix of a tree.

        Returns:
            String: Returns an infix.
        """
        if self is None:
            return ""
        if self.data == "~":
            outString = self.data + self.left.getInfix()
            return outString
        outString = ''
        if self.left is None:
            outString += self.data
        else:
            outString = ("(" + self.left.getInfix()
                         + self.data
                         + self.right.getInfix() + ")")
        outString = outString.replace('&', '^')
        outString = outString.replace('~', '¬')
        outString = outString.replace('>', '⇒')
        outString = outString.replace('=', '⇔')
        outString = outString.replace('|', '⋁')
        return outString
