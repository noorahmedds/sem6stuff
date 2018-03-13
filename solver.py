import ScrambleRubixcube as scramble
import numpy as np
from DataStructures import Node, Frontier
import time
import random
from random import randint

tng = 0
tsl = 0

# Just to see if we can get somewhere
# lets first implement dfs on our cube
# For that we need states for our cube
# Each state has 13.3(avg) children
# Every move generates a new states
# Our frontier is a stack of nodes.


def IDFS(initial_node, frontier, overall_cutoff):
    solution = ""
    for cutoff in range(0, overall_cutoff): #b/w 1 and till depth overall_Cutoff we will apply our search algorithm
        solution, _ = DLS(initial_node, [], cutoff)
        if (not solution):
            print("No solution found for depth: " + str(cutoff))
        else:
            print("Final path: " + solution)
            print("Original Scramble: " + str(scramble.my_randoms))
            break
        input("Wait for user input")


def RDS(node, frontier, limit):
    # returns goalfound

    # push current node to stack
    frontier.append(node)

    if (goal_test(node)):
        return True
    elif (limit == 0):
        return False
    else:
        cutoff_ocurred = False
        # now we generate successor
        for i in range(1, 13):
            # for IDA* here our next successor will be the best successor that could be generated which has f(n) < threshold
            # successor generated for action i
            _s = node.successor(i)
            goal_found = RDS(_s, frontier, limit-1)
            if (not goal_found):
                cutoff_ocurred = True
            elif goal_found:
                return goal_found
            frontier.pop()
        if (cutoff_ocurred):
            return goal_found


def IDAS(initial_node, frontier):
    solution = ""
    cutoff = 1
    while True: # so were checking for an infinity value as our upperbound assuming that a solutione xists
        solution, next_bound = DLS(initial_node, [], cutoff);
        if (not solution):
            print("No solution found for cost: " + str(cutoff))
            print("Next bound: " + str(next_bound) + "\n\n")
        else:
            print("Solution found for cost: " + str(cutoff))
            print("Final path: " + solution[2:])
            print("Original Scramble: " + str(scramble.my_randoms))
            global tng
            global tsl
            print ("Total Nodes explored: ", tng)
            print ("Total Successors generated: ", tsl)
            break
        # increasing the cutoff cost again
        cutoff = next_bound


def DLS(initial_node, frontier, cutoff):
    print("===============================")
    print("Running Depth limited search with cutoff: ", cutoff)
    print("===============================\n\n")

    goal_found, next_bound = RAS(initial_node, frontier, cutoff, -1)
    # do something else here
    # solution in Frontier
    solution = ""
    if (goal_found):
        # if i have found the goal then my solution is on the Frontier
        # print("yoyoyo")
        for i in range(0, len(frontier)):
            _n = frontier.pop()
            solution = str(_n.action) + " " + solution
        return solution, next_bound
    return solution, next_bound


actions= [1,2,3,4,5,6,7,8,9,10,11,12]

def RAS(node, stack, limit, next_bound):
    # returns goalfound
    # push current node to stack
    stack.append(node)
    global tng
    global tsl
    tsl += 1

    if (goal_test(node)):
        return True, next_bound
    elif (node.fn > limit):
        if (next_bound == -1):
            next_bound = node.fn
        return False, next_bound
    else:
        tng += 1
        cutoff_ocurred = False
        # random.shuffle(actions)
        for i in actions:
            # for IDA* here our next successor will be the best successor that could be generated which has f(n) < threshold
            _s = node.successor(i)
            goal_found, next_bound = RAS(_s, stack, limit, next_bound)

            if (not goal_found):
                cutoff_ocurred = True
            else:
                return goal_found, next_bound
            stack.pop()
        if (cutoff_ocurred):
            return goal_found, next_bound




def print_errythan(current_node, frontier):
    scramble.x = np.copy(current_node.state)
    print("The current state of your cube: ")
    scramble.PrintCube()

    print ("\n============== ==================== ============== \n")

    print("The frontier size: " + str(frontier.size))

    print ("\n============== ==================== ============== \n\n")


def explore_node(current_node, explored_set): #explores the current node and returns its children excluding those which have already been explored
    successors = []
    for i in range(1, 13):
        _s = current_node.successor(i)
        if (_s.state.tostring() not in explored_set):
            successors.append(_s)
    return successors


def goal_test(_node): #returns whether we have reached the goal
    if ((_node.state == scramble.xInitial).all()):
        print("GOAL FOUND")
        return True
    return False



def main():
    frontier = Frontier()
    # frontier = []
    initial_state = np.copy(scramble.x)
    initial_cost = 0
    initial_node = Node(initial_state, initial_cost, 0)

    # IDAS(initial_node, frontier)

    frontier.add(initial_node)
    expanded_set = set()

    IDFS(initial_node, frontier, 11)
    # running for multiple depths
    # for i in range(1,8):
    # for j in range(20):
        # t0 = time.time()
    # IDAS(initial_node, frontier)
        # t1 = time.time()
        # Astar(frontier, expanded_set)
        # print ("Time to run:", t1-t0)
    #
    #     scramble.x = np.array(scramble.xInitial)
    #     print("x intialized")
    #     total_move = 2
    #     my_randoms = [randint(1,12) for x in range(total_move)]
    #     for move in my_randoms:
    #         scramble.make_move(move,0,0)
    #     scramble.PrintCube()
    #     print("\n\n\n\n ================Scrambled=================\n\n\n\n\n")
    #
    #     frontier = []
    #     initial_state = np.copy(scramble.x)
    #     initial_cost = 0
    #     initial_node = Node(initial_state, initial_cost, 0)
    # print("Depth done: ", total_move, "\n\n\n\n\n\n")
    # print("")


if __name__ == '__main__':
    main()


# def Astar(frontier, explored_set):
#     current_node = frontier.pop()
#     successor = []
#
#     while (not goal_test(current_node)):
#         successors = explore_node(current_node, explored_set)
#         # we only add the node's state to the explored state because we dont need the cost to
#         # know whether if weve explored this node previously
#         explored_set.add(current_node.state.tostring())
#
#         # Iterating over all the succcessors and adding them to the frontier
#         print ("Generated " + str(len(successors)) + " successors for the current node")
#         for s in successors:
#             frontier.add(s)
#
#         # Get the next node that were going to explore
#         current_node = frontier.pop()
#
#         print_errythan(current_node, frontier)
#
#     # Print solution



# def RAS(node, stack, limit, next_bound):
#     # returns goalfound
#     # push current node to stack
#     stack.append(node)
#
#     if (goal_test(node)):
#         return True, next_bound
#     elif (node.fn > limit):
#         if (next_bound == -1):
#             next_bound = node.fn
#         return False, next_bound
#     else:
#         cutoff_ocurred = False
#         for i in range(1, 13):
#             # for IDA* here our next successor will be the best successor that could be generated which has f(n) < threshold
#             _s = node.successor(i)
#             goal_found, next_bound = RAS(_s, stack, limit, next_bound)
#
#             if (not goal_found):
#                 cutoff_ocurred = True
#             else:
#                 return goal_found, next_bound
#             stack.pop()
#         if (cutoff_ocurred):
#             return goal_found, next_bound