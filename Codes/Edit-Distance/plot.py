import matplotlib.pyplot as plt
import math
import numpy as np
x = np.arange(0.1,10, 0.1)
y_1 = (100 - x) / 10
y_2 = 1 / x
y_3 = np.log(1+np.exp(-x))
plt.plot(x, y_1, label='linear')
plt.plot(x, y_2, label='reverse')
plt.plot(x, y_3, label='log-exponential')
plt.title("Transformation Function") #添加标题
plt.legend()
plt.show()