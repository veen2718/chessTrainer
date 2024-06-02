import json

class Node:
    def __init__(self,value,children=[], parent=None):
        self.value = value
        self.children = children
        self.parent = parent
    
    def addChild(self, value):
        newChild = Node(value,parent=self)
        self.children.append(newChild)
        return newChild

    def toDict(self):
        return {self.value:[child.toDict() for child in self.children]}

def makeTree(treeDict):
    v = list(treeDict.keys())[0]
    children = [makeTree(child) for child in treeDict[v]]
    return Node(v,children)


def displayTree(tree,indent=0):
    print(" "*indent + tree.value)
    for child in tree.children:
        displayTree(child,indent+2)
