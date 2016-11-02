import fileinput

class Node:
    def __init__(self, name, parent, purity, values):
        self.name = name
        self.parent = parent
        self.purity = purity
        self.values = values

data = []
tree = []

def readData():
    input = fileinput.input()
    state = 0
    for line in input:
        if state == 3 and "%" not in line:
            data.append(line.strip("\n").split(","))
        if "@relation" in line:
            state = 1
        if "@attribute" in line:
            raw_line = line.strip("\n").split(" ")
            name = raw_line[1]
            values = raw_line[2].strip("{").strip("}").replace(" ", "").split(",")
            node = Node(name, None, None, values)
            tree.append(node)
        if "@data" in line:
            state = 3

readData()
print data
for node in tree:
    print(node.name)
    print(node.values)
