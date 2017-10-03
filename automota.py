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

    def getRowsSimplyfied(self):
        rows = self.getRows()
        firstrow = rows[0]
        rows = rows[1:]
        returnRows = []
        variables = self.findVariables(self.tree)
        variables.sort()
        signs = self.findSigns(self.tree)
        for row in rows:
            row = row[:-1]
            tempRow = row[:]
            for sign in signs:
                if sign.right is not None:
                    leftVariables = self.findVariables(sign.left)
                    rightVariables = self.findVariables(sign.right)
                    if sign.data == '&':
                        if sign.right.getResult(variables,
                                                row,
                                                sign.right) == '0':
                            for var in leftVariables:
                                tempRow[variables.index(var)] = '*'
                        elif sign.left.getResult(variables,
                                                 row,
                                                 sign.left) == '0':
                            for var in rightVariables:
                                tempRow[variables.index(var)] = '*'
                    elif sign.data == '|':
                        if sign.right.getResult(variables,
                                                row,
                                                sign.right) == '1':
                            for var in leftVariables:
                                tempRow[variables.index(var)] = '*'
                        elif sign.left.getResult(variables,
                                                 row,
                                                 sign.left) == '1':
                            for var in rightVariables:
                                tempRow[variables.index(var)] = '*'
                    elif sign.data == '>':
                        if(sign.right.getResult(
                                                rightVariables,
                                                row,
                                                sign.right) == '0'):
                            for var in leftVariables:
                                tempRow[variables.index(var)] = '*'
            tempRow.append(self.tree.getResult(variables, row, self.tree))
            returnRows.append(tempRow)
        returnRows = list(self.uniqueItems(returnRows))
        returnRows = (
                      [firstrow] +
                      returnRows
                     )
        return returnRows

    def uniqueItems(self, L):
        found = set()
        for item in L:
            if item[0] not in found:
                yield item
                found.add(item[0])

    def findSigns(self, node):
        array = []
        if node.right is not None:
            array.extend(self.findSigns(node.right))
        if node.left is not None:
            array.extend(self.findSigns(node.left))
        if node.checkIfSignIsCorrect(node.data):
            array.append(node)
        return array
        
    def findVariables(self, node):
        array = []
        if node.checkIfSignIsCorrect(node.data) is False:
            array.append(node.data)
            return list(set(array))
        else:
            if node.right is not None:
                array.extend(self.findVariables(node.right))
            if node.left is not None:
                array.extend(self.findVariables(node.left))
            return list(set(array))

    def drawFile(self):
        check_call(['dot', '-Tpng', 'tree.dot', '-o', 'outTree.png'])
