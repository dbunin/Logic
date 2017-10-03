import unittest
from automota import Automota
from node import Tree


class TestMain(unittest.TestCase):

    def test_parseString(self):
        testedClass = Automota()
        testTree = Tree('&')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('~'))
        testTree.right.addChild(Tree('B'))
        testedClass.parseString('&(A,~B)')
        self.assertEqual(testTree, testedClass.tree)

    def test_traverseTree(self):
        testedClass = Automota()
        expectedOutput = [
            'node [ fontname = "Arial" ]',
            'node1 [ label = "=" ]',
            'node1 -- node2',
            'node2 [ label = "A" ]',
            'node1 -- node3',
            'node3 [ label = "~" ]',
            'node3 -- node4',
            'node4 [ label = "B" ]']
        inputTree = Tree('=')
        inputTree.addChild(Tree('A'))
        inputTree.addChild(Tree('~'))
        inputTree.right.addChild(Tree('B'))
        result = testedClass.traverseTree(inputTree)
        self.assertEqual(expectedOutput, result)

    def test_findVariables(self):
        testedClass = Automota()
        testTree = Tree('&')
        testTree.addChild(Tree('A'))
        testTree.addChild(Tree('~'))
        testTree.right.addChild(Tree('B'))
        outArray = testedClass.findVariables(testTree)
        outArray.sort()
        self.assertEqual(outArray, ['A', 'B'])

if __name__ == '__main__':
    unittest.main()
