from node import Tree
from subprocess import check_call
import itertools


class Automota:

    def __init__(self):
        self.tree = None
        self.counter = 0

    def parseString(self, toParse, parent=None):
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
        file = open('tree.dot', 'w')
        for line in lines:
            file.write(line + '\n')
        file.close()

    def getInfix(self, tree):
        if tree is None:
            return ""
        if tree.data == "~":
            outString = tree.data + self.getInfix(tree.left)
            return outString
        outString = ("(" + self.getInfix(tree.left)
                     + tree.data
                     + self.getInfix(tree.right) + ")")
        outString = outString.replace('&', '^')
        outString = outString.replace('~', '¬')
        outString = outString.replace('>', '⇒')
        outString = outString.replace('=', '⇔')
        outString = outString.replace('|', '⋁')
        return outString

    def drawFile(self):
        check_call(['dot', '-Tpng', 'tree.dot', '-o', 'outTree.png'])
