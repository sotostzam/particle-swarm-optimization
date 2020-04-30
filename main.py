import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

# Evaluate Ackley function
def ackley(x, y, a=20, b=0.2, c=2*math.pi):
    term_1 = np.exp((-b * np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term_2 = np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
    return -1 * a * term_1 - term_2 + a + np.exp(1)

def main():
    x = np.linspace(-5, 5, 20)
    y = np.linspace(-5, 5, 20)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_surface(X, Y, ackley(X, Y), cmap='coolwarm')
    plt.show()

if __name__ == "__main__":
    main()