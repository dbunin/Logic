from node import Tree


class TruthTable:
    """
    Object to generete a coloms for a truth
    table out of a tree.

    Attributes:
        rows (List): List of rows from which the table can be genereted
        tree (Tree): object to generate a truth table from.

    Args:
        variables (List): list of variables in a tree
        tree      (Tree): object to genereta a truth
                          table from.
    """
    def __init__(self, variables, tree):
        self.rows = self.getValuesForVariables(variables)
        self.getRows(tree, variables)
        self.tree = tree

    def getValuesForVariables(self, variables):
        """
        Generate rows of truth table without results from a variables.

        Attributes:
            variables (List): list of variables.

        Returns:
            List: List of rows of truth table without results.
        """
        values = []
        value = ''
        for i in range(len(variables)):
            value = value + '0'
        for i in range(2**len(variables)):
            colom = ''
            if('b' in value):
                colom = value[2:]
                for j in range(len(variables) - len(colom)):
                    colom = '0' + colom
            else:
                colom = value
            row = list(colom)
            values.append(row)
            value = str(bin(int(value, 2) + int('1', 2)))
        return values

    def getRows(self, tree, variables):
        """
        Appends result column to a rows.

        Attributes:
            tree      (Tree): tree to generate a truth table from
            variables (List): list of variables.

        Returns:
            List: List of rows of truth table.
        """
        for row in self.rows:
            variables = variables
            row.append(tree.getResult(variables, row, tree))
        return self.rows

    def simplify(self, rows):
        """
        Simplify a truth table. Change to stars column
        values that doesn't matter on a result.

        Attributes:
            rows (List): list of rows.

        Returns:
            List: List of simplified rows of truth table.
        """
        checked = []
        new_rows = []
        for row_index, row in enumerate(rows):
            result = row[-1]
            r = row[:-1]
            for variable_index, variable in enumerate(r):
                for some_index, second_row in enumerate(rows[row_index+1:]):
                    second_row_index = some_index + row_index + 1
                    if second_row[-1] == result:
                        flag = True
                        for index in range(len(r)):
                            if (((index == variable_index and
                                    second_row[index] != variable) or
                                    second_row[index] == r[index]) is False):
                                    flag = False
                        if flag:
                            if row_index not in checked:
                                checked.append(row_index)
                            if second_row_index not in checked:
                                checked.append(second_row_index)
                            new_line = []
                            for i in range(len(r)):
                                if i == variable_index:
                                    new_line.append('*')
                                else:
                                    new_line.append(row[i])
                            new_line.append(result)
                            if new_line not in new_rows:
                                new_rows.append(new_line)
            if row_index not in checked and row not in new_rows:
                new_rows.append(row)
        if len(checked) == 0:
            return rows
        else:
            return self.simplify(new_rows)

    def getNormalForm(self, rows, variables):
        """
        Gets a normal form from a rows.

        Attributes:
            rows      (List): list of rows
            variables (List): list of variables.

        Returns:
            Tree: Normal form tree.
        """
        trees = []
        for row in rows:
            if row[-1] == '1':
                vars = []
                tempTrees = []
                for index, value in enumerate(row[:-1]):
                    if value != '*':
                        if value == '0':
                            vars.append('~' + variables[index])
                        elif value == '1':
                            vars.append(variables[index])
                for var in vars:
                    if '~' in var:
                        tempTree = Tree('~')
                        tempTree.addChild(Tree(var[1:]))
                        tempTrees.append(tempTree)
                    else:
                        tempTrees.append(Tree(var))
                trees.append(self.nodesToTree(tempTrees, '&'))
        return self.nodesToTree(trees, '|')

    def nodesToTree(self, trees, sign):
        """
        Transforms a list of nodes to tree
        and connects the nodes with sign.

        Attributes:
            trees (List): list of rows
            sign  (List): sign to connect nodes with.

        Returns:
            Tree: object of type Tree.
        """
        while len(trees) != 1:
            tree1 = trees[0]
            tree2 = trees[1]
            trees.pop(0)
            trees.pop(0)
            newTree = Tree(sign)
            newTree.addChild(tree1)
            newTree.addChild(tree2)
            trees.append(newTree)
        return trees[0]

    def getHashCode(self, rows):
        """
        Get hexadecimal code of a table.

        Attributes:
            rows      (List): list of rows.

        Returns:
            Hex: hexadecimal code of a table.
        """
        stringHashCode = ''
        for row in rows[::-1]:
            stringHashCode = stringHashCode + row[-1]
        return hex(int(stringHashCode, 2))
