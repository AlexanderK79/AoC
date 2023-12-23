import argparse
import re

class Output:
    def __init__(self, fFileContent) -> None:
        # split the file on \n\$ to get each command and output
        self.tree = Tree(TreeNode(None, None, 'd', '/', 0)) 
        self.tree.root.tree = self.tree
        commands_with_output = list(map(str.strip,('\n' + fFileContent).split('\n$')[1::]))
        # commands is a list of TreeNode, Command pairs
        # self.commands = list(map(Command, len(commands_with_output) * [self], commands_with_output))
        # loop through each command and execute it in the right position
        cur_tree_node = self.tree.root
        for cmd in commands_with_output:
            cur_tree_node = Command(cur_tree_node, cmd).tree_node
            pass
        pass

class Tree:
    # list of TreeNode items who know their own position
    def __init__(self, fNode):
        self.root = fNode

    def setRoot(self, fNode):
        self.root = fNode

    def sum_dirs(self, fNode, fResult):
        # traverse through the tree starting at fNode
        if fNode.type == 'd':
            if fNode.size <= 100000: fResult += fNode.size
            for item in fNode.children.values():
                if item.type == 'd':
                    fResult = self.sum_dirs(item, fResult)
        return (fResult)
    def list_dirs(self, fNode, fList):
        if fNode.type == 'd':
            fList += [fNode]
            for item in fNode.children.values():
                if item.type == 'd':
                    fList = self.list_dirs(item, fList)
        return (fList)

    def all(self, fNode):
        # traverse through the tree starting at fNode
        pass

class TreeNode:
    def __init__(self, fTree, fParent, fType, fName, fSize) -> None:
        self.tree = fTree
        self.type = fType # d = dir, f = file
        self.name = fName
        self.size = fSize
        P = fParent
        while P and fSize:
            P.size += fSize
            P = P.parent_node
        self.parent_node = fParent
        self.children= dict() # name of folder: TreeNode object
        pass

class Command:
    def __init__(self, fParent, fCommand) -> None:
        self.tree_node = fParent
        self.command = fCommand.split('\n')[0]
        self.output = fCommand.split('\n')[1::]
        # determine type of command
        if self.command[0:3] == 'cd ':
            # cd = navigation
            if self.command[3:4] == '/':
                self.tree_node = fParent.tree.root
            elif self.command[3:5] == '..':
                self.tree_node = fParent.parent_node
            else:
                self.tree_node = self.tree_node.children.get('_'.join(('d', self.command[3::])), TreeNode(self.tree_node.tree, self.tree_node, 0, self.command[3::], 0))
                pass
        elif self.command[0:2] == 'ls':
            # ls = list
            for c in self.output:
                type_or_size = c.split(' ')[0]
                if type_or_size == 'dir':
                    type, size = 'd', 0
                else:
                    type, size = 'f', int(type_or_size)
                name = c.split(' ')[1]
                self.tree_node.children['_'.join((type, name))] = TreeNode(self.tree_node.tree, self.tree_node, type, name, size)

            pass
        else:
            # why do we get here
            pass

class Folder:
    def __init__(self, fMessage):
        pass

class File:
    def __init__(self, fMessage):
        pass


def main(stdscr):
    with open(fName, 'r+') as f:
        data = Output(f.read())
    
    # Find all of the directories with a total size of at most 100000. 
    # What is the sum of the total sizes of those directories?
    result = data.tree.sum_dirs(data.tree.root, 0)

    message = f'The answer to part 1 is (sample should be 95437, answer should be 1390824): {result}'
    print(message)

    print(20 * '*')
    # To run the update, you need unused space of at least 30000000
    # order directories >= 70000000-30000000 by size, desc, take the first one
    size      = 70000000
    required  = 30000000
    available = size - data.tree.root.size
    required_tofree  = required - available
    result = data.tree.list_dirs(data.tree.root, [])

    result = sorted([n.size for n in result if n.size >= required_tofree])

    message = f'The answer to part 2 is (sample should be 24933642, answer should be 7490863): {result[0]}'
    print(message)


# globals
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose"   , action="store_true", default=False, help="Add this to enable verbose output")
parser.add_argument("-d", "--draw"      , action="store_true", default=False, help="Add this to enable drawing")
parser.add_argument("-i", "--drawinterval", type=int, default=1, help="Add the value in ms for drawing interval")
parser.add_argument("-p", "--production", action="store_true", default=False, help="Add this to try the puzzle input")
args = parser.parse_args()

day = '07'
fName = f'2022/input/{day}_sample.txt'
if args.production: fName = f'2022/input/{day}.txt'

debug = args.verbose
draw = args.draw

main(None)