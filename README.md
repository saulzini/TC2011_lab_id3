# TC2011 - Decision Trees Lab

## Setup

Before you begin, perform the following two steps:

- [Install autograder](https://github.com/rhomeister/autograder#for-students)
- [Setup your git repository](https://github.com/rhomeister/autograder#installation)


## Build a Decision Tree based on Data

For this lab, you're going implement the ID3 algorithm to build a decision tree 
based on a dataset.

### Objective 

Your assignment is to build a program that reads a dataset in ARFF format, and 
construct a decision tree using the ID3 algorithm. 

**Optionally for extra credit, you are also instructed to create a (G)UI to 
query the decision tree. You are free to choose the format of this program.
Create a separate script called `query` if you decide to make a program for
this. (If the script `query` is not present in your submission, it will be
assumed that you didn't do this part.)**

### Input/Output
Your program must read from `stdin` and output to `stdout`. See
[here](https://github.com/rhomeister/autograder#the-required-structure-of-a-project)
for instructions how to do this.

Basically, your program will be called by executing `run < [problem_file]`,
where `problem_file` is a file describing the problem (see below). Your program
should output the solution as text to the terminal.

**IMPORTANT: A number of testcases are provided in the testcase directory.
Make sure your program gives the exact same output on the testcases. Use
autograder or the Unix `diff` utility to check this yourself before submitting.**

#### Input

The input is given in the ARFF format. For details, see
[here](http://www.cs.waikato.ac.nz/ml/weka/arff.html). For examples, see the
`testcase` directory.

1. All attributes will be nominal (categories), not continuous.
2. The final attribute is the output field.
3. All other attributes are input.

#### Output

Output consists of the hierarchical tree, one node per line. A node is either
an internal node (a node with one or more children), or a leaf node.

These nodes should be shown in your output as follows:

1. A leaf node is an ANSWER node, and should be shown in your output as: 
   `ANSWER: [output]`. This is saying that the result of following 
   the path gives the answer `output` (for example `yes`, `no`, `maybe`).
2. An internal node is a decision node: `[attribute]: [value]`. For
   example: `outlook: sunny`. This means that the attribute `outlook` is set 
   to `sunny`.

There are a number of extra requirements:

1. All nodes need to be indented with `2 * depth` spaces. So the decision nodes
   at root level are indented with 0 spaces, and an leaf node at depth 10 with 
   20 spaces.
2. Decision nodes need to be ordered based on the occurrence of their value in
   the ARFF file. For example, if the attribute `outlook` appears in the ARFF
   file as `@attribute outlook {sunny, overcast, rainy}`, then the decision
   nodes for that attribute should appear in the order `sunny`, `overcast` and
   `rainy`.

### Example

The following example encodes a very simple dataset for the OR function:

```
@relation or

@attribute A {TRUE, FALSE}
@attribute B {TRUE, FALSE}
@attribute AorB {TRUE, FALSE}

@data
TRUE,TRUE,TRUE
FALSE,FALSE,FALSE
TRUE,FALSE,TRUE
FALSE,TRUE,TRUE
```

Output:
```
A: TRUE
  ANSWER: TRUE
A: FALSE
  B: TRUE
    ANSWER: TRUE
  B: FALSE
    ANSWER: FALSE
```

More examples can be found in the `testcases` directory
