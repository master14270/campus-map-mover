"""
Written by Jessie Smith
##########################          READ ME               #########################

- be sure to install all of the required modules to make the program run properly.
- 'main.py' and 'astar_functions.py' should be in the same directory/folder.
- all the variables discussed below are in 'astar_functions.py', modify them there.
- to move the location of the pygame window, modify 'x_pos' and 'y_pos'
- to change the number of tiles in the map, modify 'x_tiles' and 'y_tiles'
- to change the start and end points, modify 'begin_point' and 'end_point'
- to change the speed at which the display is updated, modify 'my_delay'
    (for larger maps, decrease the delay. vice-versa.)
"""

import pygame
import time
import astar_functions

# variables from other file
from astar_functions import y_tiles, x_tiles, display_w, \
    display_h, begin_point, end_point, cube_w, cube_h, my_delay, mw

# rgb color variables
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (200, 200, 200)
gold = (255, 215, 0)
orange = (255, 165, 0)

# keeping track of runtime
start_time = time.time()

# making the 2d list for the world
# world = astar_functions.make_world(y_tiles, x_tiles)
world = mw

# initializing PyGame
pygame.init()

# setting the window size and title
gameDisplay = pygame.display.set_mode((display_w, display_h))
gameDisplay.fill(black)
pygame.display.set_caption('World')


def setup_campmap():
    # putting tiles in the world.
    for i in range(y_tiles):
        for j in range(x_tiles):
            if world[i][j] == 'wall':
                world[i][j] = Tile((i, j), False)
            elif world[i][j] == 'walkable':
                world[i][j] = Tile((i, j), True)
            else:
                tmp = Tile((i, j), False)
                tmp.building = True
                tmp.draw()
                world[i][j] = tmp

    # drawing the lines.
    # astar_functions.draw_lines(gameDisplay)
    x, y = begin_point
    world[x][y].update_draw()

    # update after we are done.
    pygame.display.update()


class Tile:
    """
    This is a class to represent each node for our world.
    """

    def get_neighbors(self):
        """
        This is a function that gets then sets each neighbor of the node.
        """
        # remember, position goes row by column.
        # other attributes go column by row.
        my_i, my_j = self.position

        if self.wall:  # If it is a wall, skip. It cannot be traversed.
            return
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if y_tiles > my_i + i >= 0 and x_tiles > my_j + j >= 0:
                        self.neighbors.append((i, j))

    def draw(self):
        square = pygame.Rect(0, 0, cube_w, cube_h)

        x, y = self.coords
        x *= cube_w
        y *= cube_h

        square.topleft = (x, y)

        if self.building:
            pygame.draw.rect(gameDisplay, orange, square)
        elif self.wall:
            pygame.draw.rect(gameDisplay, black, square)
        else:
            pygame.draw.rect(gameDisplay, white, square)


    def update_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost


    def update_draw(self):

        if self.is_path:
            square = pygame.Rect(0, 0, cube_w, cube_h)

            x, y = self.coords
            x *= cube_w
            y *= cube_h

            square.topleft = (x, y)
            pygame.draw.rect(gameDisplay, grey, square)
            return

        elif self.is_closed:
            square = pygame.Rect(0, 0, cube_w, cube_h)

            x, y = self.coords
            x *= cube_w
            y *= cube_h

            square.topleft = (x, y)
            pygame.draw.rect(gameDisplay, red, square)
            return

        elif self.is_open:
            square = pygame.Rect(0, 0, cube_w, cube_h)

            x, y = self.coords
            x *= cube_w
            y *= cube_h

            square.topleft = (x, y)
            pygame.draw.rect(gameDisplay, green, square)
            return


        elif self.is_start:
            square = pygame.Rect(0, 0, cube_w, cube_h)

            x, y = self.coords
            x *= cube_w
            y *= cube_h

            square.topleft = (x, y)
            pygame.draw.rect(gameDisplay, blue, square)
            return

        elif self.is_end:
            square = pygame.Rect(0, 0, cube_w, cube_h)

            x, y = self.coords
            x *= cube_w
            y *= cube_h

            square.topleft = (x, y)
            pygame.draw.rect(gameDisplay, blue, square)
            return


    def __init__(self, pos, can_traverse=True):
        self.neighbors = []
        self.wall = not can_traverse
        self.building = False
        self.position = pos  # the position in the array
        self.coords = pos[::-1]  # position relative to the screen
        self.x_coord, self.y_coord = self.coords  # making coords more accessible

        # helpers for path-finding
        self.parent = ()
        self.g_cost = 999999  # distance from starting node
        self.h_cost = 999999  # distance from ending node
        self.f_cost = 999999  # sum of g and h cost

        # helpers for display
        self.is_start = False
        self.is_end = False
        self.is_path = False
        self.is_open = False
        self.is_closed = False

        self.get_neighbors()
        self.draw()


# setting up
setup_campmap()

# finding the path then redrawing border lines, then updating display
astar_functions.FindPath(begin_point, end_point, world, my_delay)


pygame.display.update()

# variable to keep screen up as long as necessary
user_continue = True

# calculating and printing runtime
finished = round(time.time() - start_time, 3)
print('Completed in', finished, 'seconds. Press any key to close window.')

# stay in the loop until a key is pressed.
while user_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            user_continue = False

quit()
