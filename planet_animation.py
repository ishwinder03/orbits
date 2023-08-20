import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

# Define the SolarSystem class
class SolarSystem:
    # Initialize the SolarSystem object
    def __init__(self, ax):
        self.size = 500
        self.planets = []
        self.ax = ax
        self.dT = 1

    # Add a planet to the SolarSystem
    def add_planet(self, planet):
        self.planets.append(planet)

    # Update planet positions and redraw them
    def update_planets(self):
        self.ax.clear()
        for planet in self.planets:
            planet.move()
            planet.draw()

    # Set the axis limits
    def fix_axes(self):
        self.ax.set_xlim((-self.size/2, self.size/2))
        self.ax.set_ylim((-self.size/2, self.size/2))
        self.ax.set_zlim((-self.size/2, self.size/2))

    # Calculate gravitational forces between planets
    def gravity_planets(self):
        for i, first in enumerate(self.planets):
            for second in self.planets[i+1:]:
                first.gravity(second)

# Define the Planet class
class Planet:
    # Initialize the Planet object
    def __init__(self, SolarSys, mass, position=(0, 0, 0), velocity=(0, 0, 0), color='black'):
        self.SolarSys = SolarSys
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.SolarSys.add_planet(self)
        self.color = color
        self.path = [position]
        self.boosted = False

    # Draw the planet and its path
    def draw(self):
        self.SolarSys.ax.plot(*self.position, marker="o", markersize=10, color=self.color, alpha = 0.8)
        if len(self.path) > 1:
            pre_boost_path = self.path[:62]
            post_boost_path = self.path[62:]
            self.SolarSys.ax.plot(*zip(*pre_boost_path), linestyle=':', color='red')
            if self.boosted:
                self.SolarSys.ax.plot(*zip(*post_boost_path), linestyle=':', color='blue')

    # Calculate gravitational force between two planets
    def gravity(self, other):
        distance = np.subtract(other.position, self.position)
        distanceMag = np.linalg.norm(distance)
        distanceUnit = np.divide(distance, distanceMag)
        forceMag = self.mass * other.mass / (distanceMag ** 2)
        force = np.multiply(distanceUnit, forceMag)

        switch = 1
        for body in [self, other]:
            acceleration = np.divide(force, body.mass)
            acceleration = np.multiply(force, self.SolarSys.dT * switch)
            body.velocity = np.add(body.velocity, acceleration)
            switch *= -1

    # Update the planet's position
    def move(self):
        self.position = (
            self.position[0] + self.velocity[0] * self.SolarSys.dT,
            self.position[1] + self.velocity[1] * self.SolarSys.dT,
            self.position[2] + self.velocity[2] * self.SolarSys.dT
            )
        self.path.append(self.position)

    # Boost the planet's velocity
    def boost_velocity(self, factor1, factor2, factor3):
        self.velocity = self.velocity + (factor1, factor2, factor3)
        self.boosted = True

# Define the Sun class, inheriting from Planet class
class Sun(Planet):
    # Initialize the Sun object
    def __init__(
        self,
        SolarSys,
        mass = 1000,
        position = (0, 0, 0),
        velocity = (0, 0, 0)
    ):
        super().__init__(SolarSys, mass, position, velocity)
        self.color = 'yellow'

    # Override the move method to keep the Sun stationary
    def move(self):
        pass

# Create a figure for the plots
fig = plt.figure(figsize=(21, 7))

# Create 3D subplots
ax1 = fig.add_subplot(131, projection='3d')
ax2 = fig.add_subplot(132, projection='3d')
ax3 = fig.add_subplot(133, projection='3d')

# Create three SolarSystem instances
solar_systems = [SolarSystem(ax1), SolarSystem(ax2), SolarSystem(ax3)]
value = 2.5
boost_factors = [
    (value, 0, 0),
    (0, value, 0),
    (0, 0, value)
]

# Create planets and suns for each solar system
planets = []
suns = []

for ss in solar_systems:
    planet = Planet(ss, mass=10, position=(100, 0, 0), velocity=(0, 10, 0), color='blue')
    sun = Sun(ss)
    planets.append(planet)
    suns.append(sun)

# Define the animation function
def animate(i):
    for ss, planet, boost_factor, axis, direction in zip(solar_systems, planets, boost_factors, [ax1, ax2, ax3], ['x', 'y', 'z']):
        ss.gravity_planets()
        if i == 62:
            planet.boost_velocity(*boost_factor)

        ss.update_planets()
        ss.fix_axes()
        axis.set_title(f'Velocity boost in {direction} direction')

# Create the animation
anim = animation.FuncAnimation(fig, animate, frames=500, interval=1)

# Set the writer for the animation and save it as a video file (optional)
writervideo = animation.FFMpegWriter(fps=60)
#anim.save("planets_animation.mp4", writer=writervideo, dpi=200)
plt.show()