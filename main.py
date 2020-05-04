import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np

# Particle class
class Particle():
    def __init__(self, x, y, z, velocity):
        self.pos = [x, y]
        self.pos_z = z
        self.velocity = velocity
        self.best_pos = self.pos.copy()

class Swarm():
    def __init__(self, pop, v_max):
        self.particles = []             # List of particles in the swarm
        self.best_pos = None            # Best particle of the swarm
        self.best_pos_z = math.inf      # Best particle of the swarm

        for _ in range(pop):
            x = np.random.uniform(-5, 5)
            y = np.random.uniform(-5, 5)
            z = cost_function(x, y)
            velocity = np.random.rand(2) * v_max
            particle = Particle(x, y, z, velocity)
            self.particles.append(particle)
            if self.best_pos != None and particle.pos_z < self.best_pos_z:
                self.best_pos = particle.pos.copy()
                self.best_pos_z = particle.pos_z
            else:
                self.best_pos = particle.pos.copy()
                self.best_pos_z = particle.pos_z

# Evaluate objective/cost function (Ackley)
def cost_function(x, y, a=20, b=0.2, c=2*math.pi):
    term_1 = np.exp((-b * np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term_2 = np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
    return -1 * a * term_1 - term_2 + a + np.exp(1)

def main():
    dimensions = 2              # Number of dimensions
    max_iterations = 100        # Maximum Iterations
    B_LO = -5                   # Upper boundary
    B_HI = 5                    # Upper boundary
    PERSONAL_C = 2.5            # Personal Acceleration Coefficient
    SOCIAL_C = 1.7              # Social Acceleration Coefficient
    GLOBAL_BEST = 0             # Global Best of Cost function
    CONVERGENCE = 0.01          # Convergence value
    population = 20             # Particle Swarm Size
    v_max = 0.1                 # Max Particle Velocity

    # Initialize plotting variables
    x = np.linspace(B_LO, B_HI, 50)
    y = np.linspace(B_LO, B_HI, 50)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(10,5))

    # Initialize swarm
    swarm = Swarm(population, v_max)

    curr_iter = 0
    while curr_iter < max_iterations and abs(swarm.best_pos_z - GLOBAL_BEST) > CONVERGENCE:
        for particle in swarm.particles:

            for i in range(0, dimensions):
                r1 = np.random.uniform(0, 1)
                r2 = np.random.uniform(0, 1)
                
                # Update particle's velocity
                particle.velocity[i] += PERSONAL_C * r1 * (particle.best_pos[i] - particle.pos[i]) + SOCIAL_C * r2 * (swarm.best_pos[i] - particle.pos[i])

                # Check if velocity is exceeded
                if particle.velocity[i] > v_max:
                    particle.velocity[i] = v_max
                if particle.velocity[i] < -v_max:
                    particle.velocity[i] = -v_max

            # Update particle's current position
            particle.pos += particle.velocity
            particle.pos_z = cost_function(particle.pos[0], particle.pos[1])

            # Update swarm's best known position
            if particle.pos_z < swarm.best_pos_z:
                swarm.best_pos = particle.pos.copy()
                swarm.best_pos_z = particle.pos_z

            # Update particle's best known position
            if particle.pos_z < cost_function(particle.best_pos[0], particle.best_pos[1]):
                particle.best_pos = particle.pos.copy()

            # Check if particle is within boundaries
            if particle.pos[0] > B_HI:
                particle.pos[0] = np.random.uniform(B_LO, B_HI)
                particle.pos_z = cost_function(particle.pos[0], particle.pos[1])
            if particle.pos[1] > B_HI:
                particle.pos[1] = np.random.uniform(B_LO, B_HI)
                particle.pos_z = cost_function(particle.pos[0], particle.pos[1])
            if particle.pos[0] < B_LO:
                particle.pos[0] = np.random.uniform(B_LO, B_HI)
                particle.pos_z = cost_function(particle.pos[0], particle.pos[1])
            if particle.pos[1] < B_LO:
                particle.pos[1] = np.random.uniform(B_LO, B_HI)
                particle.pos_z = cost_function(particle.pos[0], particle.pos[1])

        plt.clf()
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        axc = fig.add_subplot(1, 2, 2)
        ax.plot_surface(X, Y, cost_function(X, Y), cmap='winter')
        axc.contourf(X, Y, cost_function(X, Y))
        for particle in swarm.particles:
            ax.scatter(particle.pos[0], particle.pos[1], particle.pos_z, marker='*', c='r')
            axc.scatter(particle.pos[0], particle.pos[1], marker='*', c='r')
            axc.arrow(particle.pos[0], particle.pos[1], particle.velocity[0], particle.velocity[1], head_width=0.05, head_length=0.1, fc='k', ec='k')
        plt.pause(0.001)

        curr_iter += 1
    plt.show()

if __name__ == "__main__":
    main()