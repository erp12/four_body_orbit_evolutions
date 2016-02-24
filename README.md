# four_body_orbit_evolutions

Python application that finds stable orbits of 4 masses useing a genetic algorithm.

Uses the package DEAP for the genetic algorithum.
Also requires SciPy for the simulation of gravitational system.
Running Anaconda version of Python is recomended.

More README coming soon.

## About this project
This project began as a final project for NS204: Physics 1, which I decided to make more relevant to my concentration. The initial assignment was to create a simulation of planetary bodies that orbit each other without colliding. This involved finding planetary masses that, when given the correct initial positions and velocities, would enter stable orbits around each other when a gravity simulation was applied. I initially used the R programming language to complete this task.

A potential application of evolutionary computation, a method of creating Artificial Intelligence, became apparent in this assignment. Each planetary body had 3 properties that served as inputs to the simulation. These properties are, the bodies mass, initial position, and initial velocity. Finding values for these properties that producing stable orbital patterns is essentially an optimization problem, which evolutionary computation is quite adept at solving.

I chose to limit my problem to 4 planetary bodies, and used a simple genetic algorithm to find the values for each bodies mass, initial position, and initial velocities. I chose to implement the genetic algorithm in the Python programming language, using the DEAP (Distributed Evolutionary Algorithms in Python) package. I used the PyGame package to draw visualizations of the simulations.

This project was my first 'hands on' experience with creating a multi-objective genetic algorithm. Initially I used a very simple fitness function, which calculated the closest each body got its initial position and velocity, during the second half of the simulation. Evolution produced simulations with near zero error based on this fitness function very quickly, but it was not the desired result. DEAP discovered that if every planetary body was very far apart, and had very little mass, the gravitational force between the planets would be very small, and the planets would barely move over the course of the simulation. They did not produce any collisions, and the planetary bodies ended up very close to their initial position. This caused me to write a second fitness function, which calculated the closest each body's velocity got to the exact opposite direction of its initial velocity. Combining these two fitness functions in a way that would guide evolution to produce stable orbits was quite difficult at first. I tried multiple different methods of combining the two fitness functions. I found that in this instance, having both functions be treated equal worked best.

The best final result that I was able to reproduce was to get three out of four planetary bodies completing near-perfect orbits, but evolution could never optimize all four. The main lesson I learned during this project is that even seemingly simple optimizations can be very difficult, and evolution an be a difficult system to control. If I were to re-create this problem again, I would likely choose a more mathematical approach, specifically one of the optimization methods found in the field of Statistical Learning.
