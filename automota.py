from node import Tree
from subprocess import check_call


class Automota:
    """
    Object to generete a tree out of string
    and manipulate the tree.

    Args:
        tree       (Tree): a tree object genereted
                           from user's input
        counter    (int): a counter
    """
    def __init__(self):
        self.tree = None
        self.counter = 0

    def parseString(self, toParse, parent=None):
        """
        Change to default comparing to the Object.

        Attributes:
            toParse (String): users inputed ASII string
            parent  (Tree): Node of a tree
        """
        komaIndex = toParse.find(',')
        if komaIndex == -1:
            notIndex = toParse.find('~')
            tempTree = None
            if notIndex != -1:
                if notIndex != 0:
                    raise ValueError
                else:
                    toParse = toParse.replace(')', '')
                    toParse = toParse.replace('(', '')
                    tempTree = Tree(toParse[0])
                    tempTree.addChild(Tree(toParse[1:]))
            else:
                toParse = toParse.replace(')', '')
                toParse = toParse.replace('(', '')
                tempTree = Tree(toParse)
            if self.tree is None:
                self.tree = tempTree
            else:
                parent.addChild(tempTree)
            return toParse
        else:
            while toParse[:komaIndex + 1].count('(') != (
                    toParse[:komaIndex].count(',') + 1):
                newIndex = toParse[komaIndex + 1:].find(',') + 1
                komaIndex += newIndex
                if newIndex == -1:
                    raise ValueError()
            sign = toParse[0]
            tree = Tree(sign)
            if self.tree is None:
                self.tree = tree
            else:
                parent.addChild(tree)
            left = self.parseString(toParse[2:komaIndex], tree)
            right = self.parseString(toParse[komaIndex+1:-1], tree)
            if left == -1 or right == -1 or (
                    not tree.checkIfSignIsCorrect(sign)):
                raise ValueError()

    def traverseTree(self, tree, parentCounter=None):
        """
        Generate a dot string for dot file.

        Attributes:
            tree          (Tree): The object to traverse
            parentCounter (int): the number of parents.

        Returns:
            List: The rows to write a dot file.
        """
        if tree is None:
            return ['']
        resultArray = []
        self.counter += 1
        if parentCounter is None:
            resultArray.append('node [ fontname = "Arial" ]')
            resultArray.append('node1 [ label = "' + tree.data + '" ]')
        else:
            resultArray.append('node' + str(parentCounter) + ' -- node'
                               + str(self.counter))
            resultArray.append('node' + str(self.counter) +
                               ' [ label = "' + tree.data + '" ]')
        counter = self.counter
        resultArray = (resultArray +
                       self.traverseTree(tree.left, counter))
        resultArray = (resultArray +
                       self.traverseTree(tree.right, counter))
        return list(filter(('').__ne__, resultArray))

    def writeToFile(self, lines):
        """
        Function to write lines to a file.

        Attributes:
            lines (List): The rows of string to write to file.
        """
        file = open('tree.dot', 'w')
        for line in lines:
            file.write(line + '\n')
        file.close()

    def drawFile(self):
        """
        Creates a png file from a dot file.
        """
        check_call(['dot', '-Tpng', 'tree.dot', '-o', 'outTree.png'])
