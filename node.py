import json

class Node:
    def __init__(self,value,children=[], parent=None):
        self.value = value
        self.children = children
        self.parent = parent
    
    def addChild(self, value):
        values = [child.value for child in self.children]
        if value in values:
            return self.children[values.index(value)]
        newChild = Node(value,parent=self,children=[])
        self.children.append(newChild)
        print(newChild.children)
        return newChild

    def toDict(self):
        return {self.value:[child.toDict() for child in self.children]}
    
    def getOrigin(self):
        n = self
        while n.parent != None:
            n = n.parent
        return n

def makeTree(treeDict,parent=None):
    v = list(treeDict.keys())[0]
    children = [makeTree(child,parent) for child in treeDict[v]]

    node0 = Node(v,children,parent)

    for child in children:
        child.parent = node0

    return node0


def displayTree(tree,indent=0):
    print(" "*indent + tree.value)
    for child in tree.children:
        displayTree(child,indent+2)

# tree_dict = {
#     "root": [
#         {"child1": [
#             {"subchild1": []},
#             {"subchild2": []}
#         ]},
#         {"child2": []}
#     ]
# }

# node1 = makeTree(tree_dict)
# displayTree(node1)
# print("\n")
# node1 = node1.children[0]
# displayTree(node1)
# print("\n")
# node1 = node1.children[1]
# displayTree(node1)
# print("\n")
# node2 = node1.addChild("subSubchild")
# displayTree(node2)
# displayTree(node1)
# print("\n")
# displayTree(node2.parent)
# displayTree(node2.getOrigin())


# node1 = Node("root")
# node1 = node1.addChild('child1')
# displayTree(node1.getOrigin())