#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np

x_data = [100, 83, 71, 63, 56, 50, 42, 33, 25, 24, 22, 20]
y_data = [0, -0.5, -1, -1.5, -2, -2.5, -3.5, -5, -7.5, -8, -9, -10]

poly = np.polyfit(x_data, y_data, deg=6)
poly_func = np.poly1d(poly)
print(poly_func)
print(poly_func(100))

plt.plot(x_data, y_data, 'o')

plt.plot(np.arange(0, 100, 1), np.polyval(poly, np.arange(0, 100, 1)))

plt.show()
