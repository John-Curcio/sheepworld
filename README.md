## Dependencies
Python 3, pygame, NumPy

## Instructions

To run the simulation and watch an animation, enter the following command in your terminal:

`python sheepWorld.py`

Soon, I'm going to provide the option for a user to specify simulation parameters such as sheep speed, number of parents, and the maximum complexity of a sheep's strategy. So for now, it'll just run with some default parameters.

## Introduction
This is an expansion of my 112 Term Project. I've become a much better programmer since then, but I'm still enthralled with the phenomenon of learners adapting to each other's learning progress, so I've made some improvements. 

Besides being a confirmation of the [selfish herd theory](https://en.wikipedia.org/wiki/Selfish_herd_theory), this project is analogous to applications of game theory - for example, when AIs compete on the stock market for arbitrage.

## Outline
Sheepworld is a world where sheep are stranded on a meadow planet where a wolf randomly appears, kills the first sheep it can get to, then disappears, and so on. When the population dips below a certain threshold, a round of breeding occurs, and the cycle renews. The sheep have strategies that dictate their paths, and these are passed on to new sheep by sexual reproduction.

After only a few minutes spent on sheepworld, you'll probably notice that the sheep are quick learners. The image below is a typical arrangement of the sheep population at generation 5 or so. They're so young that they haven't even realized that wolves are dangerous!

![early](early\ \stages.JPG)

After about 20 generations, though, not only do the sheep turn tail from the wolf without hesitation - the sheep have discovered that there is *great safety in numbers and close quarters.* 

![later](selfish\ \herd.JPG)

## Some more notes:

On Sheepworld, sheep may have more than 2 parents.

Sheepworld is effectively a torus, so sheep don't need to be aware of their absolute positions, only their relative positions.

On sheepworld, a sheep may have more than two parents, and it's possible for a sheep to be a parent more than once to the same child (i.e. contributes more genes).

The mutation rate on sheepworld is inversely proportional to the genetic diversity among the child sheep's parents. This is [similar](https://en.wikipedia.org/wiki/Simulated_annealing) (very loosely) to simulated annealing, where approximate global optima are obtained by accepting less "fit" solutions after convergence, as a way of escaping global minima.
