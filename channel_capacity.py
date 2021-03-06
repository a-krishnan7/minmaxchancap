#! /usr/bin/python

#import libraries
from matplotlib import pyplot as plt
import numpy as np
import random
from scipy import optimize
import math

#Pyhy[i,j] signifies the probability that the predicted class i is chosen given that the true class is j
#Pyh[i] signifies the probability that an object is predicted to be in class i
#Py[j] is the probability that a random object is from class j

#initialize a test matrix
def Initializer(r, n):
    matrix = np.random.rand(n,n)
    np.fill_diagonal(matrix, 0)
    matrix /= matrix.sum(axis=1, keepdims = True)
    matrix *= 1-r
    np.fill_diagonal(matrix, r)
    return matrix

def Deriver(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    dx = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
                if calcPyh(inputArray, n, Py)[i] == 0.0:
                    return "why"
                a = (Py[j] * np.log2((Pyhy_i[i,j] / calcPyh(inputArray, n, Py)[i])))
                b = (1/math.log(2))
                c = (1/math.log(2)) * (1/calcPyh(inputArray, n, Py)[i])
                dx[i,j] = a + b - c
    return np.ravel(dx)

def FixedDeriver(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    denom_sum = Pyhy_i.dot(Py)
    return np.ravel(Py * np.log2(Pyhy_i / denom_sum))
    
#Calculate Pyh[i] given n, Pyhy, and Py using the formula sigma(index j) P(Yhi|Yj)*P(Yj)
def calcPyh(inputArray, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    Pyh = Pyhy_i.dot(Py)
    return Pyh

#calculate c given Pyhy, Py, Pyh using the formula for channel capacity (without the supremum)
def chCapMinIterative(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    chanCap = 0.0
    Pyh_i = calcPyh(Pyhy_i, n, Py)
    for i in range(n):
        for j in range(n):
            inParenPrimer = Pyhy_i[i,j]/Pyh_i[i]
            if inParenPrimer > 0:
                inParen = math.log(inParenPrimer, 2)
                a = float(Pyhy_i[i,j])
                b = float(Py[j])
                d = float(inParen)
                c = a*b*d
                chanCap = chanCap + c
    return chanCap

def chCapMaxIterative(inputArray, r, n, Py):
    return -chCapMinIterative(inputArray, r, n, Py)
    
    
def chCapMin(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n, n)
    Pyh_i = calcPyh(Pyhy_i, n, Py)
    nonzero = np.nonzero(Pyh_i)
    ratio = Pyhy_i[nonzero]/Pyh_i[nonzero]
    joint = Pyhy_i[nonzero]*Py[np.newaxis, :]
    nonzero = np.nonzero(joint)
    return np.sum(joint[nonzero] * np.log2(ratio[nonzero]))

def chCapMax(inputArray, r, n, Py):
    return -chCapMin(inputArray, r, n, Py)

#constraint 1 (con1) was removed and replaced by the 'bounds' method in minimize.fmin_slsqp 

#constraint 2: sum of Pyhy elements in a row is np.sum(Pyhy_i[i]) = 1.0
def con2(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    row_wise = (Pyhy_i.sum(axis=1)-1)**2
    return np.sum(row_wise)

#constraint 3: fixed classification accuracy, summation(index i) of Pyhy * Py = r
def con3(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    diag = np.diag(Pyhy_i)
    return diag.dot(Py) - r
    
#this is the constraint that makes Pyhy[i,i] > Pyhy[i,j]
def con4(inputArray, r, n, Py):
    Pyhy_i = inputArray.reshape(n,n)
    Pyhy_diag = np.diag(Pyhy_i)
    Pyhy_max = Pyhy_i.max(axis=1)
    diff = Pyhy_diag - Pyhy_max
    worst_case = diff.min()
    return worst_case
