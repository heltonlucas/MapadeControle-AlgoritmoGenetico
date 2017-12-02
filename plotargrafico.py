# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 12:16:49 2017

@author: helto
"""
import xlrd
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


dataset = "ParametrosAG.xlsx"
workbook = xlrd.open_workbook(dataset)
sheet = workbook.sheet_by_index(0)

x=[]
y=[]
z=[]

#for line in dataset:
#    line = line.strip()
#    X,Y,Z = line.split(',')
#    x.append(X)
#    y.append(Y)
#    z.append(Z)
for row in range(sheet.nrows):

    x.append(sheet.cell_value(row, 0))
    y.append(sheet.cell_value(row, 1))
    z.append(sheet.cell_value(row, 2))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, c='blue')

ax.set_xlabel('Populaçao')
ax.set_ylabel('Crossover')
ax.set_zlabel('Pressão de Seleção')

plt.show()




