

class TruthTable:
    def __init__(self, variables, tree):
        self.rows = self.getValuesForVariables(variables)
        self.getRows(tree, variables)
        self.tree = tree

    def getValuesForVariables(self, variables):
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
        for row in self.rows:
            variables = variables
            row.append(tree.getResult(variables, row, tree))
        return self.rows

    def simplify(self, rows):
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
        normalForm = '('
        for row in rows:
            if len(normalForm) != 1 and normalForm[-1] != '(':
                normalForm = normalForm + '|('
            if row[-1] == '1':
                for index, value in enumerate(row[:-1]):
                    if value != '*':
                        if value == '0':
                            normalForm = normalForm + '~' + variables[index]
                        elif value == '1':
                            normalForm = normalForm + variables[index]
                        normalForm = normalForm + '&'
                while normalForm[-1] == '&':
                    normalForm = normalForm[:-1]
                normalForm = normalForm + ')'
        return normalForm

    def getHashCode(self, rows):
        stringHashCode = ''
        for row in rows[::-1]:
            stringHashCode = stringHashCode + row[:-1]
        return int(stringHashCode, 2)
