import fileinput
import math
import re

data = []
attributes = []

def readData():
    input = fileinput.input()
    global goal_key
    state = 0
    for line in input:
        if state == 1 and "%" not in line:
            data.append(line.strip("\n").split(","))
        if "@attribute" in line:
            raw_line = re.sub('\s+', '', line)
            raw_list = raw_line.replace("@attribute", "").strip("}").split("{")
            attributes.append(raw_list[0])
        if "@data" in line:
            state = 1

def defaultize_attr(attrs, data, tarAttr):
    countD = {}
    index = attrs.index(tarAttr)
    for vector in data:
        if vector[index] in countD:
            countD[vector[index]] += 1.0
        else:
            countD[vector[index]] = 1.0
    maxVal = 0
    defaultValue = None
    for key in countD.keys():
        if countD[key] > maxVal:
            maxVal = countD[key]
            defaultValue = key
    return defaultValue

def entropy(attrs, d, tarAttr):
    countD = {}
    currentEntropy = 0.0
    index = 0
    for attr in attrs:
        if (tarAttr == attr):
            break
        ++index
    for vector in data:
        if (countD.has_key(vector[index])):
            countD[vector[index]] += 1.0
        else:
            countD[vector[index]]  = 1.0

    for value in countD.values():
        currentEntropy += -(value/len(data)) * math.log(value/len(data), 2)

    return currentEntropy

def info_gain(attrs, data, attr, tarAttr):
    countD = {}
    currentEntropy = 0.0
    index = attrs.index(attr)
    for vector in data:
        if countD.has_key(vector[index]):
            countD[vector[index]] += 1.0
        else:
            countD[vector[index]]  = 1.0
    for value in countD.keys():
        prob = countD[value] / sum(countD.values())
        subset = [vector for vector in data if vector[index] == value]
        currentEntropy += prob * entropy(attrs, subset, tarAttr)
    return (entropy(attrs, data, tarAttr) - currentEntropy)

def choose_best(data, attrs, tarAttr):
    bestAttr = attrs[0]
    gain = 0;
    for attr in attrs:
        newGain = info_gain(attrs, data, attr, tarAttr)
        if newGain > gain:
            gain = newGain
            bestAttr = attr
    return bestAttr

def get_values(data, attrs, bestAttr):
    values = []
    index = attrs.index(bestAttr)
    for vector in data:
        if vector[index] not in values:
            values.append(vector[index])
    return values

def get_subset(data, attrs, bestAttr, value):
    subset = [[]]
    index = attrs.index(bestAttr)
    for vector in data:
        if vector[index] == value:
            newVec = []
            for i in range(0, len(vector)):
                if i != index:
                    newVec.append(vector[i])
            subset.append(newVec)
    subset.remove([])
    return subset

def id3(data, attrs, tarAttr):
    dataset = data[:]
    print(attrs)
    values = [vector[attrs.index(tarAttr)] for vector in dataset]
    defaultValue = defaultize_attr(attrs, dataset, tarAttr)
    if not dataset or len(attrs) - 1 <= 0:
        return defaultValue
    elif values.count(values[0]) == len(values):
        return values[0]
    else:
        bestAttr = choose_best(dataset, attrs, tarAttr)
        tree = {bestAttr: {}}
        for value in get_values(dataset, attrs, bestAttr):
            subset = get_subset(dataset, attrs, bestAttr, value)
            newAttrs = attrs[:]
            newAttrs.remove(bestAttr)
            subtree = id3(subset, newAttrs, tarAttr)
            tree[bestAttr][value] = subtree
    return tree

readData()
print attributes, data
targetAttr = attributes[-1]
decisionTree = id3(data, attributes, targetAttr)
print(decisionTree)
