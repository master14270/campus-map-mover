# What is campus-map-mover?
This is a python project that uses the a-star pathfinding algorithm to find the shortest path between any two points of interest on campus.

# How do I run it?
First, make sure you have the required dependencies. The only one you should have to install is 'pygame' which is used to display what is going on clearly.
Once you have all the dependencies, just run 'main.py'.

# Can I customize this?
Yes you can! The 'config.ini' file allows you to change some of the constants.
If you would like to use a different map, all you have to do is make sure you store the map in a .csv file, where each cell is a 'tile' on your map.
Each cell should contain a tuple, corresponding to the rgb values of the pixel from the map.
Then you will have to input the file name into the config file. 
