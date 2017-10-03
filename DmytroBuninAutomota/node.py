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
