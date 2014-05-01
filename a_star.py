class Problem(object):
	def heuristic(self, point, goal):
		return 0
	
	def neighbor_nodes(self, point):
		return []
	
	def distance_between_neighbors(self, point, point2):
		return 1

	def is_goal(self, point, goal):
		return point == goal

	def on_open(self, point, f, g, h):
		pass
	
	def on_close(self, point):
		pass

	def on_update(self, point, f, g, h):
		pass


class PathNotFound(Exception):
	pass

def find_path(problem, start, goal):
	'''
	Finds a path from point start to point goal using the A* algorithm.
	'''

	# set up a clean slate for this pass of the algorithm.
	# The open set contains points at the perimeter: we know how to reach
	# these points from the start, but have not yet explored all their neighbors.
	open_set = set()

	# the open_queue contains the same points as the open_set, but associates them
	# with their f-score, and indeed is kept ordered by f-score. This lets
	# us quickly choose the most promising points in the open set to explore next.
	# It technically obviates the open_set but as an implementation detail it's
	# easier to store them separately and use the set to check for membership
	# and the queue to keep them sorted by f-score.
	open_queue = list()

	# The closed set contains points that we are finished with and won't visit
	# again. We know how to reach them from start but have already explored
	# all their neighbors.
	closed_set = set()

	# The came_from dict is a map from each point to one of it's neighbors.
	# You can think of it as a vector field flowing back to the start. If you
	# iteratively follow the 
	came_from = dict()

	# the g-score is the currently best known cost to reach each point. It
	# is syncronized with the came_from vector field: if you followed it all
	# the way back to the start, the cost would be exactly value found in g-score
	# for that point. It isn't necessarily the best possible way to get to that
	# point, just the best way we've discovered so far.
	g_score = dict()

	# the h-score is the estimate for how far away from the goal this point
	# is, as estimated by the problem's heuristic function.
	h_score = dict()

	# f can be computed rather than stored.
	def f_score(point):
		return g_score[point] + h_score[point]

	# we can kick off the algorithm by placing only the start point in the open set.
	g_score[start] = 0
	h = problem.heuristic(start, goal)
	h_score[start] = h
	open_set.add(start)
	open_queue.append( (f_score(start), start) )
	problem.on_open(start, h, 0, h)

	# keep searching until we find the goal, or until all possible pathes have been exhausted.
	while open_set:
		open_queue.sort()
		next_f, point = open_queue.pop(0)
		open_set.remove(point)

		if problem.is_goal(point, goal):
			# reached goal, unwind path
			path = [ point ]
			while point != start:
				point = came_from[point]
				path.append(point)
			path.reverse()
			return path

		closed_set.add(point)
		problem.on_close(point)

		for neighbor in problem.neighbor_nodes(point):
			if not neighbor in closed_set:
				tentative_g_score = g_score[point] + problem.distance_between_neighbors(neighbor, point)

				if neighbor not in open_set:
					# new territory to explore
					came_from[neighbor] = point
					g = tentative_g_score
					h = problem.heuristic(neighbor, goal)
					g_score[neighbor] = g
					h_score[neighbor] = h
					open_set.add(neighbor)
					f = g + h
					open_queue.append( (f, neighbor) )
					problem.on_open(neighbor, f, g, h)

				else:
					# reconnected to previously explored area
					if tentative_g_score < g_score[neighbor]:
						# but we found a better route than before!
						came_from[neighbor] = point
						g = tentative_g_score
						g_score[neighbor] = g
						h = problem.heuristic(neighbor, goal)
						h_score[neighbor] = h
						f = g + h
						
						problem.on_update(neighbor, f, g, h)

	raise PathNotFound("no path from %s to %s." % (str(start), str(goal)))



