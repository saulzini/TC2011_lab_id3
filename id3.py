import fileinput
import math
import copy
import re

class Attribute:
    def __init__(self, label, index, values):
        self.label = label
        self.index = index
        self.values = values

data = []
attributes = []

def readData():
    input = fileinput.input()
    global goal_key
    state = 0
    index = 0
    for line in input:
        if state == 1 and "%" not in line:
            data.append(line.strip("\n").split(","))
        if "@attribute" in line:
            raw_line = re.sub('\s+', '', line)
            raw_list = raw_line.replace("@attribute", "").strip("}").split("{")
            goal_key = raw_list[0]
            new_attr = Attribute(raw_list[0], index, raw_list[1].split(","))
            index += 1
            attributes.append(new_attr)
        if "@data" in line:
            state = 1

def entropy(attrs, target_attr, data):
    countDictionary = {}
    index = attrs.index(target_attr)
    totalValues = len(data)
    for i in range(0, len(data)):
        if data[i][index] in countDictionary:
            countDictionary[data[i][index]] += 1.0
        else:
            countDictionary[data[i][index]] = 1.0
    entropy = 0
    for key, value in countDictionary.items():
        entropy -= (value/totalValues) * math.log(value/totalValues, 2)
    return entropy

def infoGain(attrs, data, attr, target_attr):
    countDictionary = {}
    index = attrs.index(attr)
    gain = 0.0
    for i in range(0, len(data)):
        if data[i][index] in countDictionary:
            countDictionary[data[i][index]] += 1.0
        else:
            countDictionary[data[i][index]] = 1.0
    for key, value in countDictionary.items():
        probability = value / sum(countDictionary.values())
        subset = [vector for vector in data if vector[index] == key]
        gain += probability * entropy(attrs, target_attr, subset)
    return entropy(attrs, target_attr, data) - gain

def choose_best(data, attrs, target_attr):
    gain = 0
    best_attr = attrs[0]
    for attr in attrs:
        if attr.label != target_attr.label:
            attr_gain = infoGain(attrs, data, attr, target_attr)
            if attr_gain > gain:
                gain = attr_gain
                best_attr = attr
    return best_attr

def defaultize_attr(attrs, data, target_attr):
    default = ""
    maxCount = 0
    index = attrs.index(target_attr)
    countDictionary = {}
    for vector in data:
        if vector[index] in countDictionary:
            countDictionary[vector[index]] += 1.0
        else:
            countDictionary[vector[index]] = 1.0
    for key in countDictionary.keys():
        if countDictionary[key] > maxCount:
            maxCount = countDictionary[key]
            default = key
    return default

def get_subset(data, attrs, bestAttr, value):
    subset = [[]]
    index = attrs.index(bestAttr)
    for vector in data:
        if vector[index] == value:
            newVector = []
            for i in range(0, len(vector)):
                if i != index:
                    newVector.append(vector[i])
            subset.append(newVector)
    subset.remove([])
    return subset

def id3(data, attrs, target_attr):
    dataset = copy.deepcopy(data)
    values = target_attr.values
    defaultValue = defaultize_attr(attrs, data, target_attr)
    if not dataset or len(attrs) - 1 <= 0:
        return defaultValue
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        bestAttr = choose_best(dataset, attrs, target_attr)
        tree = {bestAttr.label:{}}
        for value in bestAttr.values:
            subset = get_subset(data, attrs, bestAttr, value)
            newAttr = attrs[:]
            newAttr.remove(bestAttr)
            subtree = id3(subset, newAttr, target_attr)
            tree[bestAttr.label][value] = subtree
    return tree

def print_tree(tree, indent):
    print(tree)


readData()
decisionTree = id3(data, attributes, attributes[len(attributes) - 1])
print_tree(decisionTree, 0)
