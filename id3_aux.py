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

def entropy(target_attr, data):
    countDictionary = {}
    index = target_attr.index
    totalValues = len(data)
    for i in range(0, len(data)):
        if data[i][index] in countDictionary:
            countDictionary[data[i][index]] += 1
        else:
            countDictionary[data[i][index]] = 1.0
    entropy = 0
    for key, value in countDictionary.items():
        entropy -= (value/totalValues) * math.log(value/totalValues, 2)
    return entropy

def infoGain(data, attr, target_attr):
    countDictionary = {}
    index = attr.index
    gain = 0.0
    for i in range(0, len(data)):
        if data[i][index] in countDictionary:
            countDictionary[data[i][index]] += 1.0
        else:
            countDictionary[data[i][index]] = 1.0
    for value in countDictionary.keys():
        probability = countDictionary[value] / sum(countDictionary.values())
        subset = [vector for vector in data if vector[index] == value]
        gain += probability * entropy(target_attr, subset)
    return entropy(target_attr, data) - gain

def choose_best(data, attrs, target_attr):
    gain = 0
    best_attr = None
    for attr in attrs:
        if attr.label != target_attr.label:
            attr_gain = infoGain(data, attr, target_attr)
            if attr_gain > gain or len(attrs) < 3:
                gain = attr_gain
                best_attr = attr
    return best_attr

def defaultize_attr(data, target_attr):
    default = ""
    maxCount = 0
    index = target_attr.index
    countDictionary = {}
    for i in range(0, len(data)):
        if data[i][index] in countDictionary:
            countDictionary[data[i][index]] += 1.0
        else:
            countDictionary[data[i][index]] = 1.0
    for key, value in countDictionary.items():
        if value > maxCount:
            maxCount = value
            default = key
    return default


def id3(data, attrs, target_attr, indent):
    dataset = copy.deepcopy(data)
    values = target_attr.values
    defaultValue = defaultize_attr(data, target_attr)
    indentation = ""
    for i in range(0, indent):
        indentation += " "
    if not dataset or len(attrs) - 1 <= 0:
        print(indentation + "ANSWER: " + defaultValue)
    elif len([value[target_attr.index] for value in dataset if value[target_attr.index] == value[0]]) == len(values):
        print(indentation + "ANSWER: " + values[0])
    else:
        bestAttr = choose_best(dataset, attrs, target_attr)
        for value in bestAttr.values:
            print(indentation + bestAttr.label + ": " + value)
            for vector in data:
                if vector[bestAttr.index] == value:
                    subset = [test for test in data if test[bestAttr.index] == value]
                    indent += 2
                    id3(subset, [attr for attr in attrs if attr.label != bestAttr.label], target_attr, indent)
                    indent -= 2

readData()
id3(data, attributes, attributes[len(attributes) - 1], 0)
