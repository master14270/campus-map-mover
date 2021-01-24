import configparser

myConfig = configparser.ConfigParser()
myConfig.read("settings.ini")

hold = myConfig['Constants']['starting_point']

print(hold)
if hold:
    print("Not null")
else:
    print("Null")


