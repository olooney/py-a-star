import a_star

class Stacks(object):
    def __init__(self, stacks):
        if isinstance(stacks, Stacks):
            self.stacks = stacks.stacks
        else:
            self.stacks = stacks

    @staticmethod
    def make_start(number_of_pegs):
        stack_list = [ [] for peg in xrange(number_of_pegs) ]
        if stack_list:
            stack_list[0] = range(number_of_pegs, 0, -1)
        return Stacks(stack_list)

    @staticmethod
    def make_goal(number_of_pegs):
        stack_list = [ [] for peg in xrange(number_of_pegs) ]
        if stack_list:
            stack_list[-1] = range(number_of_pegs, 0, -1)
        return Stacks(stack_list)

    def copy(self):
        return Stacks( [ list(stack) for stack in self.stacks ])

    def is_legal(self):
        for stack in self.stacks:
            supporting_block = 999
            for block in stack:
                if block >= supporting_block:
                    return False
                else:
                    supporting_block = block
        return True

    def depth(self, index):
        return len(self.stacks[index])

    def move(self, from_index, to_index):
        new_stacks = self.copy()
        from_stack = new_stacks.stacks[ from_index ]
        to_stack = new_stacks.stacks[ to_index ]
        to_stack.append(from_stack.pop())
        return Stacks(new_stacks)

    def __unicode__(self):
        return 'Stacks(%s)' % repr(self.stacks)

    def __repr__(self):
        return 'Stacks(%s)' % repr(self.stacks)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)


class HanoiProblem(a_star.Problem):
    def __init__(self, pegs=3):
        self.number_of_pegs = pegs

    def neighbor_nodes(self, stacks):
        neighbors = []

        for i in xrange(self.number_of_pegs):
            for j in xrange(self.number_of_pegs):
                if i != j and stacks.depth(i) > 0:
                    neighbor = stacks.move(i, j)
                    if neighbor.is_legal():
                        neighbors.append(neighbor)
        return neighbors
    
    def heuristic(self, position, goal):
        # number of blocks successfully moved to the last peg
        return len(position.stacks[-1]) 
    
if __name__ == '__main__':
    import sys
    if len(sys.args) == 1:
        number_of_pegs = 3
    else:
        number_of_pegs = int(sys.args[1])

    hanoi = HanoiProblem(number_of_pegs)

    # the "points" in the HanoiProblem are of type "Stacks",
    # so the we need to instantiate Stacks for the start and ends points.
    start = Stacks.make_start(number_of_pegs)
    goal = Stacks.make_goal(number_of_pegs)

    # then a miracle occurs...
    solution = a_star.find_path(hanoi, start, goal)

    for position in solution:
        print position 

