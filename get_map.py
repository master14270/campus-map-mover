import csv
import configparser

# This is the configuration file
myConfig = configparser.ConfigParser()
myConfig.read("settings.ini")

# Reading the csv
datafile = open(myConfig['Constants']['file_to_read'], 'r')
datareader = csv.reader(datafile, delimiter=',')

camp_map = []
for row in datareader:
    camp_map.append(row)

# Here, we remove some of the outer rows and columns of the map, to make it easier to see.
del camp_map[:150]  # removing top 150 rows
del camp_map[300:]  # removing rows from 300 to bottom

# keeping columns ranging from 40 to 340
camp_map = [l[40:340] for l in camp_map]

my_world = []
row_num = len(camp_map)
col_num = len(camp_map[0])

for i in range(row_num):
    row = []
    for j in range(col_num):
        row.append('')
    my_world.append(row)

POI = []  # points of interest
for i in range(row_num):
    for j in range(col_num):
        info = camp_map[i][j]
        info = info.strip('[]')
        info = info.split(', ')
        info = tuple(int(x) for x in info)

        r, g, b = info
        # max = 765
        if r + g + b >= 750:
            my_world[i][j] = 'walkable'
        elif r > 250 and g + b < 20:
            my_world[i][j] = 'building'
        elif b > 250 and r + g < 20:  # found entrance
            POI.append((i, j))
            my_world[i][j] = 'walkable'
        else:
            my_world[i][j] = 'wall'

# close the file when we are done.
datafile.close()
