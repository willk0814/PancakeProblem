"""Solve the burnt pancake problem with both BFS and A* search methods
   Author: David W. Clendenning Jr.
"""
from operator import methodcaller
import queue

class Node:

# assign the state, string of value to the state, and if the pancake has been flipped or not to the object
# in addition calculate the cost based on the flipped pancake (if flipped) and assign the children / parent to the node in question
# chilren will be a dictionary with key-value of state_string: child
  def __init__(self, state, state_string, children, flip_value=None):
    self.state = state
    self.state_string = state_string
    self.flip_value = flip_value
    if flip_value != None:
      self.cost = self.flip_value + 1
    else:
      self.cost = None
    self.parent = None
    self.children = children

# helper function to find the value of a nodes state based on replacing characters with numerical values in order to break a tie of equivalent positions
  def get_tie_breaker_value(self):
    state_string = "".join(self.state)
    state_string = state_string.replace('w', '1').replace('b', '0')
    return int(state_string)

# add child node to an existing node
  def add_node(self, child):
    self.children.update({child.state_string: child})
    child.parent = self


# converts the input string into the problem statement requirements and parses it according to pancakes and search type
def input_to_pancakes(s_input):
  start_state = [s_input[i:i+2] for i in range(0, len(s_input), 2)]
  search_type = start_state.pop(len(start_state)-1)
  return start_state, search_type

# using a specified state we will use this function to acquire the next state
def get_next_state(start_node_state, flip_value):
# we will copy our state from the start node into our next state value
  next_state = list.copy(start_node_state.state)
# following this copy function we will flip the pancakes over and use list comprehension to reverse the array
  next_state[0:flip_value+1] = next_state[0:flip_value+1][::-1]
# reassign either white or burnt to the states of the pancakes
  for i in range(0, flip_value+1):
    if 'b' in next_state[i]:
      next_state[i] = next_state[i].replace('b', 'w')
    elif 'w' in next_state[i]:
      next_state[i] = next_state[i].replace('w', 'b')
# return node that represents the "next" state from where we "started"
  return Node(next_state, "".join(next_state), {}, flip_value=flip_value)#+1?

# get_possible_next_states shows the 4 states possible by flipping at any value 1-4's pancake flip value
""" the example below is flipping at value of 2 pancakes so 1b2b3b4b will become 2w1w3b4b
      ___                                 -------
    _______             -->                 ---
  ___________                           -----------
_______________                       ---------------

"""
def get_possible_next_states(state_node):
# create empty array to store possible states
  possible_next_states = []
# traverse the possible states of flipping the top pancake, then the next state will be the top pancake + 1, etc.
# ex:
  for i in range(0, len(state_node.state)):
    possible_next_state = get_next_state(state_node, i)
# add all four possible states to the list and return
    possible_next_states.append(possible_next_state)
  return possible_next_states



# check to see if the state is the solution
def solution_state_check(state):
  return state == ['1w', '2w', '3w', '4w']

def heuristic_largest_pancake_out_of_place(state):
  # define the heuristic from the class
  # loop through all pancakes
  for i in range(4): # from 0 - 3 for pancakes so we will use i+=1 / 3-i to confirm pancake position
# assign pancake value to state number of the pancake
# because we are looking for the largest number of pancakes out of place
    pancake_in_place = int(state[3-i][0])
    pancake_out_of_place = int(4-i)
    if(pancake_in_place!=pancake_out_of_place):
        return pancake_out_of_place
  return 0

# calculate all edges costs (from parents costs) and add it all up to the total cost and return it as the new g value for the respective node
def get_total_path_cost(state_node):
  current_node = state_node
  t_cost = 0
  while current_node.parent != None:
    t_cost += current_node.cost
    current_node = current_node.parent
  return t_cost

# returns solution in string form such that it conforms to the problem specifications
def get_solution(goal_node, print_costs=False):
  state_list = []
  current_node = goal_node
  spatula_value = None
  while current_node.parent != None:
# get g, h value from the respective functions that calculate those values. We will use these values to print the problem solution.
    g = get_total_path_cost(current_node)
    h = heuristic_largest_pancake_out_of_place(current_node.state)
    cost_string = ""
# insert spatula at the flip_index value to show in the problem solution
    if spatula_value != None:
      current_node.state.insert(spatula_value, '|')
# if we are using A* search we will print the g and h values along with the rest of the result
    if print_costs:
      #cost_string += " g:" + str(g) + ", h:" + str(h)
      cost_string += a_star_format(cost_string, g, h)
    state_list.append("".join(current_node.state)+cost_string)
# change the spatula value so we can focus on the next node
    spatula_value = current_node.flip_value+1
    current_node = current_node.parent
  g = get_total_path_cost(current_node)
  h = heuristic_largest_pancake_out_of_place(current_node.state)
  cost_string=""
  if print_costs:
    #cost_string += " g:" + str(g) + ", h:" + str(h)
    cost_string += a_star_format(cost_string, g, h)
  current_node.state.insert(spatula_value, '|')
  state_list.append("".join(current_node.state)+cost_string)
# reverse order because we started at a child node rather than a parent and we climbed up the tree
  state_list=state_list[::-1]
  solution = ""
# we just append each state to a single string with a new line operator and return this string to be printed
  for state_string in state_list:
    solution += state_string + "\n"
  return solution

# a helper function to show the format of A*
def a_star_format(cost_string, g, h):
  return " g:" + str(g) + ", h:" + str(h)

# A*'s search function we use with the heuristic "largest pancake out of place"
def a_star_search_function(start_state):
# enqueue base node (root)
  tree_root = Node(start_state, "".join(start_state), {})
  g = 0
# initialize fringe and add base root node to it
  fringe = []
  fringe.append((g + heuristic_largest_pancake_out_of_place(start_state), tree_root))
# keep track of the visited nodes for efficiency
  visited = set()
# make sure the fringe is not empty
  while len(fringe) > 0:
# sort based on f value to always pop off the *LEAST* value'd f node and then the tie_breaker helper function
    fringe.sort(key=lambda x: (x[0], get_tie_breaker_value(x[1])))
# dequeue our node to expand and add to our visited (where fringe = open_set, and visited = closed_set)
    node_to_expand = fringe.pop(0)
    visited.add(node_to_expand[1].state_string)
# if the state we are in is the solution we will return the solution with the help of our solution finder function (that returns the string)
    if(solution_state_check(node_to_expand[1].state)):
      print("solution:\n")
      solution = get_solution(node_to_expand[1], print_costs=True)
      #print(solution)
      return solution
# if we are not in the solution we will check all possible next states for the next node to expand
    else:
      possible_next_states = get_possible_next_states(node_to_expand[1])
# if a child node is already visited --> do not revisit
      for node in possible_next_states:
        if node.state_string in visited:
          possible_next_states.remove(node)
# for all remaining possible next states (child nodes), we will begin expanding them and adding to the fringe with the format [f, node]
      for new_state_node in possible_next_states:
        node_to_expand[1].add_node(new_state_node)
        fringe.append((get_total_path_cost(new_state_node) + heuristic_largest_pancake_out_of_place(new_state_node.state), new_state_node))
# if no solution --> return error
  return "Error: unable to find solution"

# checks for tie breaker based on if two states are equivalent, we will replace the burnt or un-burnt index's with a 0, 1 respectively
def get_tie_breaker_value(self):
  state_string = "".join(self.state)
  state_string = state_string.replace('w', '1').replace('b', '0')
  return int(state_string)

# Breadth-First_Search's function declaration
def bfs_search_function(start_state):
# create tree node root
  tree_root = Node(start_state, "".join(start_state), {})
# create FIFO fringe and enqueue the root node
  fringe = queue.Queue()
  fringe.put(tree_root)
  visited = set()
  nodes_visited = 0
  while not fringe.empty():
# expand node and add to the visited set (a.k.a closed_set)
    node_to_expand = fringe.get()
    visited.add(node_to_expand.state_string)
# if we have found the solution, return
    if solution_state_check(node_to_expand.state):
      print("solution:\n")
      solution = get_solution(node_to_expand, print_costs=False)
      return solution
# if we have not found the solution, we will look at the next possible states first pruning all "visited" states
    else:
      possible_next_states = get_possible_next_states(node_to_expand)
      for node in possible_next_states:
        if node.state_string in visited:
          possible_next_states.remove(node)
# tie breaker function that make sure no two nodes who have positions of equal value get misplaced
      possible_next_states.sort(key=methodcaller("get_tie_breaker_value"))
# begin next node to be expanded
      for new_state_node in possible_next_states:
        node_to_expand.add_node(new_state_node)
        fringe.put(new_state_node)
  return "Error: unable to find solution"

# this function ask for a problem state description (e.g. 1b2b3b4b-a) and run the respective search function (bfs or A*)
# this state of sorts is represented as a tuple as defined in the "input_to_pancakes" function (e.g. (['1b','2b','3b','4b'], '-a')
def run_search():
  problem = input("please enter a search string for the burnt pancake problem\n\n")
  start_state, search_type = input_to_pancakes(problem)
  #print(search_type)

  if(search_type == '-b'):
    return bfs_search_function(start_state)
  elif(search_type == '-a'):
    return a_star_search_function(start_state)
  else:
    print("invalid search / start state type")

# main function
if __name__ == "__main__":
  search_solution = run_search()
  print(search_solution)
