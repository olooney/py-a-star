Abstract A* Algorithm
---------------------

Provides an implementation of the fundamental A* algorithm that uses Python
dynamic typing to abstract it away from the details of any particular problem.
To solve a real-world problem, all that is necessary is to describe it
declaratively by implementing the Problem interface, and then call solve_path()
to apply the A* algorithm to find a path from the starting state to the goal
state. Two specific Problem examples are provided to show how it can be adapted
to different problems: the classic 2D path-finding problem, and the less
obvious Towers of Hanoi problem. Examples of other problems ammenable to A* in
very abstract spaces are rubics cubes and automated theorem proving.

While A* is interesting in itself, the main purpose of this snippet is to
demonstrate how Python's dynamic typing and implicit interfaces enable a very
high degree of generic programming. The algorithm does not place any
limitations at all on what a "point" is: it can be anything: a tuple of
integers representing a coordinate position, a string representing a
proposition, the complete "game state" of a puzzle.

It also shows how productive the paradigm of mapping problems to a domain where
they can be tackled by powerful algorithms.  The GridProblem class defined in
solve_maze, for example, is only a few dozen lines of straight-forward, almost
declarative code. And yet the A*-powered solver is incredibly powerful.
