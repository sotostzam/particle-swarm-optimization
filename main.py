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
        self.best_pos = self.pos

class Swarm():
    def __init__(self, pop, v_max):
        self.particles = []             # List of particles in the swarm
        self.best_pos = None            # Best particle of the swarm
        self.best_pos_z = math.inf          # Best particle of the swarm

        for _ in range(pop):
            x = np.random.uniform(-3, 3)
            y = np.random.uniform(-3, 3)
            z = ackley(x, y)
            velocity = np.random.rand(2) * v_max
            particle = Particle(x, y, z, velocity)
            self.particles.append(particle)
            if self.best_pos != None and particle.pos_z < self.best_pos_z:
                self.best_pos = particle.pos
                self.best_pos_z = particle.pos_z
            else:
                self.best_pos = particle.pos
                self.best_pos_z = particle.pos_z

# Evaluate Ackley function
def ackley(x, y, a=20, b=0.2, c=2*math.pi):
    term_1 = np.exp((-b * np.sqrt(0.5 * (x ** 2 + y ** 2))))
    term_2 = np.exp((np.cos(c * x) + np.cos(c * y)) / 2)
    return -1 * a * term_1 - term_2 + a + np.exp(1)

def main():
    dimensions = 2              # Number of dimensions
    max_iterations = 100        # Maximum Iterations
    PERSONAL_C = 2.5            # Personal Acceleration Coefficient
    SOCIAL_C = 1.7              # Social Acceleration Coefficient
    GLOBAL_BEST = 0             # Global Best of Cost function
    CONVERGENCE = 0.01          # Convergence value
    population = 20             # Particle Swarm Size
    v_max = 0.1                 # Max Particle Velocity

    # Initialize plotting variables
    x = np.linspace(-3, 3, 50)
    y = np.linspace(-3, 3, 50)
    X, Y = np.meshgrid(x, y)
    fig = plt.figure(figsize=(10,5))

    # Initialize swarm
    swarm = Swarm(population, v_max)

    curr_iter = 0
    while curr_iter < max_iterations and abs(swarm.best_pos_z - GLOBAL_BEST) > CONVERGENCE:
        r1 = np.random.uniform(0, 1)
        r2 = np.random.uniform(0, 1)

        for particle in swarm.particles:
            # Update particle's velocity
            particle.velocity[0] += (PERSONAL_C * r1 * (particle.best_pos[0] - particle.pos[0])) + (SOCIAL_C * r2 * (swarm.best_pos[0] - particle.pos[0]))
            particle.velocity[1] += (PERSONAL_C * r1 * (particle.best_pos[1] - particle.pos[1])) + (SOCIAL_C * r2 * (swarm.best_pos[1] - particle.pos[1]))

            # Check if velocity is exceeded
            if particle.velocity[0] > v_max:
                particle.velocity[0] = v_max
            if particle.velocity[0] < -v_max:
                particle.velocity[0] = -v_max
            if particle.velocity[1] > v_max:
                particle.velocity[1] = v_max
            if particle.velocity[1] > -v_max:
                particle.velocity[1] = -v_max

            # Update particle's position
            particle.pos[0] += particle.velocity[0]
            particle.pos[1] += particle.velocity[1]
            particle.pos_z = ackley(particle.pos[0], particle.pos[1])

            # Update swarm's best known position
            if particle.pos_z < swarm.best_pos_z:
                swarm.best_pos = particle.pos
                swarm.best_pos_z = particle.pos_z
                print("New best swarm position: " + str(swarm.best_pos_z))

            # Update particle's best known position
            if ackley(particle.pos[0], particle.pos[1]) < swarm.best_pos_z:
                #print("New best position")
                particle.best_pos = particle.pos

            # Check if particle is within boundaries
            if particle.pos[0] > 3 or particle.pos[1] > 3:
                particle.pos[0] = np.random.uniform(-3, 3)
                particle.pos[1] = np.random.uniform(-3, 3)
                particle.pos_z = ackley(particle.pos[0], particle.pos[1])
            if particle.pos[0] < -3 or particle.pos[1] < -3:
                particle.pos[0] = np.random.uniform(-3, 3)
                particle.pos[1] = np.random.uniform(-3, 3)
                particle.pos_z = ackley(particle.pos[0], particle.pos[1])

        plt.clf()
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        axc = fig.add_subplot(1, 2, 2)
        ax.plot_surface(X, Y, ackley(X, Y), cmap='coolwarm')
        axc.contourf(X, Y, ackley(X, Y))
        for particle in swarm.particles:
            ax.scatter(particle.pos[0], particle.pos[1], particle.pos_z, marker='*', c='r')
            axc.scatter(particle.pos[0], particle.pos[1], marker='*', c='r')  
        plt.pause(0.001)

        curr_iter += 1
    plt.show()

if __name__ == "__main__":
    main()