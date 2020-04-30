import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from random import random

# Evaluate Ackley function
def ackley(x, y, a=20, b=0.2, c=2*math.pi):
    term_1 = np.exp((-b * np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term_2 = np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
    return -1 * a * term_1 - term_2 + a + np.exp(1)

def main():
    dimensions = 2              # Number of dimensions
    max_iterations = 100        # Maximum Iterations
    c1 = 2.5                    # Personal Acceleration Coefficient
    c2 = 1.7                    # Social Acceleration Coefficient
    global_best = 0             # Global Best of Cost function
    population = 20             # Particle Swarm Size
    swarm_gbest = [0, 0]        # Best swarm potition
    swarm_gbest_z = math.inf    # Best swarm potition on z
    v_max = 0.1                 # Max Particle Velocity

    # Initialization
    swarm = -3 + np.random.rand(population, 2) * 6
    velocity = np.random.rand(population) * v_max
    output = ackley(swarm[:,0], swarm[:,1])

    for _ in range(0, max_iterations):
        r1 = random()
        r2 = random()

    x = np.linspace(-5, 5, 20)
    y = np.linspace(-5, 5, 20)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_surface(X, Y, ackley(X, Y), cmap='coolwarm')
    ax.scatter(swarm[:,0], swarm[:,1], output, marker='*')
    plt.show()

if __name__ == "__main__":
    main()