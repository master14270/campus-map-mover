import pygame
import time
import operator
import os
import math
import random

from get_map import row_num, col_num, POI, myConfig
from get_map import my_world as mw

# setting window position.
x_pos = int(myConfig['Constants']['window_x_position'])
y_pos = int(myConfig['Constants']['window_y_position'])
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x_pos, y_pos)

# how many tiles are in the world in x and y directions.
x_tiles = col_num
y_tiles = row_num

# how many seconds to wait between each draw attempt.
my_delay = float(myConfig['Constants']['draw_delay'])

# setting the start and end points for the map (make sure they are in a tuple!)
if myConfig['Constants']['starting_point'] and myConfig['Constants']['ending_point']:
    raw_txt = myConfig['Constants']['starting_point'].split()
    begin_point = tuple([int(x) for x in raw_txt])

    raw_txt = myConfig['Constants']['ending_point'].split()
    end_point = tuple([int(x) for x in raw_txt])
else:
    begin_point = random.choice(POI)
    end_point = random.choice(POI)

# creating display variables for the size of the window
display_w = int(myConfig['Constants']['window_width'])
display_h = int(myConfig['Constants']['window_height'])


# the dimensions of each cube/tile
cube_w = display_w / x_tiles
cube_h = display_h / y_tiles

cube_size_diagonal = math.sqrt(cube_w**2 + cube_h**2)

# creating color variables
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (200, 200, 200)
gold = (255, 215, 0)
orange = (255, 165, 0)


def draw_lines(display):
    """
    Draws the lines separating the tiles on the map.
    :param display: the display to be drawn on.
    """

    # drawing vertical lines
    for i in range(1, x_tiles + 1):
        start = cube_w * i
        pygame.draw.line(display, grey,
                         (start, 0),
                         (start, display_h))

    # drawing horizontal lines
    for j in range(1, y_tiles + 1):
        start = cube_h * j
        pygame.draw.line(display, grey,
                         (0, start),
                         (display_w, start))


def Get_Distance(nodeA, nodeB):
    """
    This function calculates the distance (in pixels) between two points.
    :param nodeA: the first node.
    :param nodeB: the second.
    :return: float: the distance (in pixels) between nodeA and nodeB.
    """

    # first, we get the distance of each component separately
    distX = abs(nodeA.x_coord - nodeB.x_coord)
    distY = abs(nodeA.y_coord - nodeB.y_coord)

    # from here, there are only two possibilities.
    # either the x distance is longer, or the y distance is longer.
    # (if they are equal, either calculation would suffice.)
    # knowing this, we can create a formula for each case.

    if distX > distY:  # for the first case:
        # we travel diagonally the y distance
        # then we travel horizontally the x distance,
        # minus the distance from y that we already traveled.
        return cube_size_diagonal * distY + cube_w * (distX - distY)
    else:
        # we travel diagonally the x distance
        # then we travel vertically the y distance,
        # minus the distance from x that we already traveled.
        return cube_size_diagonal * distX + cube_h * (distY - distX)


def Retrace_Path(start, end):
    """
    takes in two points, using their parents, retraces the path.
    :param start: the starting point.
    :param end: the ending point.
    :return: a list of each node in order from 'start', to 'end'.
    """
    path = []
    current = end

    # we start at the end.
    # first we append the node to the 'path'
    # then, we reset the node to the nodes parent.
    # we repeat this until we reach the starting node.
    while current != start:
        path.append(current)
        current = current.parent

    # this process doesn't actually add the starting node!
    # so we just add it manually.
    path.append(start)

    # this process gives us the path from end to beginning.
    # we want the path from beginning to end!
    # so we reverse it before returning it.
    path.reverse()
    return path


def FindPath(start_pos, end_pos, my_world, delay=0.0):
    """
    This is a function that finds the shortest path between two points.
    :param start_pos: the starting point.
    :param end_pos: the ending point.
    :param my_world: the map to be traversed.
    :param delay: how many seconds between draw updates.
    short delay = fast updates
    long delay = slow updates
    """

    # first, we need to declare the starting and ending nodes.
    tmp1, tmp2 = start_pos
    start_node = my_world[tmp1][tmp2]

    tmp1, tmp2 = end_pos
    end_node = my_world[tmp1][tmp2]

    # for clarity, we redraw both of these nodes.
    start_node.is_start = True
    start_node.update_draw()

    end_node.is_end = True
    end_node.update_draw()

    pygame.display.update()

    # next, we need to store the 'open' and 'closed' nodes.
    open_nodes = []
    closed_nodes = []

    # now, we add the starting node to the open nodes.
    open_nodes.append(start_node)

    # we initialize the respective costs of for the start node.
    start_node.g_cost = 0
    start_node.h_cost = Get_Distance(start_node, end_node)
    start_node.f_cost = start_node.g_cost + start_node.h_cost

    # while there are nodes to be evaluated:
    while len(open_nodes) > 0:

        # finding the node with the lowest f cost
        # f cost = g cost + h cost
        # g cost is distance from start node
        # h cost is distance from end node
        lowest = open_nodes[0]
        lowest_idx = 0
        for i in range(1, len(open_nodes)):
            if (open_nodes[i].f_cost < lowest.f_cost) or\
                    ((open_nodes[i].f_cost == lowest.f_cost) and # if the nodes have the same f cost
                     (open_nodes[i].h_cost < lowest.h_cost)): # take the node with the lower h cost
                lowest = open_nodes[i]
                lowest_idx = i

        # take current from open to closed, then add it to closed nodes.
        current = open_nodes[lowest_idx]
        closed_nodes.append(open_nodes.pop(lowest_idx))

        # we want to draw whenever we add a new closed node
        current.is_closed = True
        current.is_open = False
        current.update_draw()
        pygame.display.update()
        time.sleep(delay)

        # we have found the end, exit
        if current == end_node:
            path = Retrace_Path(start_node, end_node)
            # print('Shortest path from', start_pos, 'to', end_pos)
            # print('Drawing now...')
            for item in path:
                item.is_path = True
                item.update_draw()
                pygame.display.update()
                time.sleep(delay)
            return True

        # checking if each neighbor is a wall, or if it is closed.
        # if so, go to the next neighbor.
        for neighbor in current.neighbors:
            # we store the neighbors relatively.
            # this means the top right neighbor would be stored as: (-1, 1) (row, col)
            # so in order to get the position of the neighbor, we need to do some calculating.
            # we just add the current position, to the neighbors to get the desired result.
            neighbor_pos_i, neighbor_pos_j = tuple(map(operator.add, current.position, neighbor))
            true_neighbor = my_world[neighbor_pos_i][neighbor_pos_j]

            # if the node is a wall or it is closed, skip it.
            if true_neighbor.wall or (true_neighbor in closed_nodes):
                continue

            # we are getting the g cost here.
            newMoveCostToNeighbor = current.g_cost + Get_Distance(current, true_neighbor)

            # if this cost is shorter than the one on file,
            # or the node is not already in open nodes:
            if (newMoveCostToNeighbor < true_neighbor.g_cost) or (true_neighbor not in open_nodes):
                # set the g and h cost
                true_neighbor.g_cost = newMoveCostToNeighbor
                true_neighbor.h_cost = Get_Distance(true_neighbor, end_node)
                true_neighbor.update_f_cost() # set f cost
                true_neighbor.parent = current # set parent

                # if true neighbor is not in open nodes, add it, then we draw it.
                if true_neighbor not in open_nodes:
                    open_nodes.append(true_neighbor)
                    true_neighbor.is_open = True
                    true_neighbor.update_draw()
                    pygame.display.update()
                    time.sleep(delay)

    # if we get out of this loop without finding a path, there is no path
    print('There is no path to the exit. :(')
    return False