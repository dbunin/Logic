import unittest
from TruthTable import TruthTable
from node import Tree


class TestTruthTable(unittest.TestCase):
    def test_getValuesForVariables(self):
        testTree = Tree('&')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('~'))
        testTree.right.addChild(Tree('B'))
        testedClass = TruthTable(['A', 'B'], testTree)
        expectedValue = [['0', '0'], ['0', '1'], ['1', '0'], ['1', '1']]
        values = testedClass.getValuesForVariables(['A', 'B'])
        self.assertEqual(expectedValue, values)

    def test_getRows(self):
        testTree = Tree('&')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('~'))
        testTree.right.addChild(Tree('B'))
        testedClass = TruthTable(['A', 'B'], testTree)
        expectedValue = [
                         ['0', '0', '0'],
                         ['0', '1', '0'],
                         ['1', '0', '1'],
                         ['1', '1', '0']
                        ]
        self.assertEqual(expectedValue, testedClass.rows)

    def test_simplify(self):
        testTree = Tree('|')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('|'))
        testTree.right.addChild(Tree('B'))
        testTree.right.addChild(Tree('C'))
        testedClass = TruthTable(['A', 'B', 'C'], testTree)
        expectedValue = [
                         ['0', '0', '0', '0'],
                         ['*', '*', '1', '1'],
                         ['*', '1', '*', '1'],
                         ['1', '*', '*', '1'],
                        ]
        values = testedClass.rows
        simplified_table = testedClass.simplify(values)
        self.assertEqual(expectedValue, simplified_table)

    def test_getNormalForm(self):
        testTree = Tree('>')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('B'))
        testedClass = TruthTable(['A', 'B'], testTree)
        values = testedClass.rows
        simplified_table = testedClass.simplify(values)
        normalForm = testedClass.getNormalForm(simplified_table,
                                               ['A', 'B'])
        expectedTree = Tree('|')
        expectedTree.addChild(Tree('~'))
        expectedTree.addChild(Tree('B'))
        expectedTree.left.addChild(Tree('A'))
        self.assertEqual(expectedTree, normalForm)


if __name__ == '__main__':
    unittest.main()
