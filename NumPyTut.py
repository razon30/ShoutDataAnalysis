# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:36:34 2020

@author: Razon
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 3 * np.pi, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.plot(x,y_sin)
plt.plot(x, y_cos)
plt.xlabel('x Axis')
plt.ylabel('Y Axis')
plt.title('Sine Cosine')
plt.legend(['Sine' , 'Cosine'])
plt.show()


a = np.zeros(2)
print(a)


a = np.array([1,2,3])
print(a[0])
print(a.shape)
a[0] = 0
print(a)

b = np.array([[1,2,3],[4,5,6]])
print(b)
print(b.shape)