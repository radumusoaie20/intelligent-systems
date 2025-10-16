import numpy as np
import matplotlib.pyplot as plt

A = 3
f = 5
fi= np.pi / 3
x = np.arange(0, 1, 0.025)

y_sin = A*np.sin(2*f*x + fi)


plt.plot(x, y_sin, 'o:r', markersize=5)
plt.xlabel('t(s)')
plt.ylabel('A(m)')
plt.title('Sinusoidal signal function')
plt.grid()
plt.show()