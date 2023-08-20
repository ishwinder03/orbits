# orbits
Brief Description:
The primary goal of my program was to visualize the gravitational interactions of a single planet orbiting the Sun under the influence of the inverse-square law, while also observing the effects of velocity boosts in the x, y, and z directions. I displaying three separate animations side by side to view the planetary motion due to different velocity boosts. Initially, the planet follows a circular orbit with the Sun at its center. However, upon applying the velocity boosts in the x, y, or z direction, the initial orbit becomes non-circular and adopts an elliptical shape, with the Sun now positioned at one of the foci instead of the center.

A problem occurred due to trajectories too close to the Sun which caused the planets to be slinghshotted off the grid. This was solved by selecting appropriate initial conditions for position/velocity. Another challenge was determining the appropriate frame at which the orbit completed a full rotation of 2π to apply the speed boost. This is most likely due to the numerical accuracy of the algorithm and the timestep used in the simulation.

