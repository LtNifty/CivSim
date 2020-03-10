from graphics import *
import random
#####################################
#            B I O M E S            #
#####################################
class Biome:
    name = ""
    taken = False
    owner = None

    def getName(self):
        return self.name

    def getTaken(self):
        return self.taken

    def getOwner(self):
        return self.owner
    
    def setTaken(self, isTaken):
        self.taken = isTaken

    def setOwner(self, Civilization):
        self.owner = Civilization

class Ocean(Biome):
    def __init__(self):
        self.name = "Ocean"

class Plains(Biome):
    def __init__(self):
        self.name = "Plains"

class CivTile(Rectangle, Biome):
#####################################
#     C I V I L I Z A T I O N S     #
#####################################
class Civilization:
    name = ""
    color = ""

    def getName(self):
        return self.name
    
    def getColor(self):
        return self.color
    
class Ronin(Civilization):
    def __init__(self):
        self.name = "Ronin"
        self.color = "white"

class Slythe(Civilization):
    def __init__(self):
        self.name = "Slythe"
        self.color = "red"

class Bumbumopolis(Civilization):
    def __init__(self):
        self.name = "Bumbumopolis"
        self.color = "yellow"
        
#####################################
#              M A I N              #
#####################################

# Prompts to enter map size and other game settings
def preGameSettings():
    win = GraphWin("Civilization Simulation", 500, 100, autoflush=False)
    text1 = Text(Point(250, 25), "How many tiles long do you want the map to be? (5 <= x <= 30)")
    text1.draw(win)
    text2 = Text(Point(250, 75), "Press \"ENTER\" when you're ready.")
    text2.draw(win)

    entry = Entry(Point(250, 50), 2)
    entry.draw(win)

    global mapSize
    while (win.getKey() != "Return"): # User must hit "ENTER" to continue
        mapSize = int(entry.getText())
    win.close()
        
# Calculates the pixel size and offset to fit all squares in 500x500 frame
def calcPixelSize():
    global pixelSize, offset
    offset = 20 # x black pixels on all sides; gives space for row/col numbers
    i = 0
    while(mapSize * i <= 500 - 2 * offset):
        i += 1
    pixelSize = i - 1
    offset += int((500 - mapSize * pixelSize) / 2 - offset) # I have no idea why this works lol
        
# Generates random list of Plains and Ocean && creates world map
def genWorldMap():
    print("Creating map...")
    global worldMap
    worldMap = [[0 for i in range(mapSize)] for j in range(mapSize)] # Creates 'x' lists each with 'x' placeholders
    for i in range (0, mapSize):
        for j in range(0, mapSize):
            if (random.randint(0,1) == 1): # Randomly decides if tile will be Plains or Ocean
                worldMap[i][j] = Ocean()
            else:
                worldMap[i][j] = Plains()

    numSize = 7 # int(pixelSize / 2)
    if (pixelSize / 2 > 12):
        numSize = 12
    elif (pixelSize / 2 < 7):
        numSize = 7

    for i in range(0, mapSize):
        number = Text(Point(int(offset/2), 50 + offset + i * pixelSize + pixelSize/2), str(i + 1)) # Creates row numbers
        number.setTextColor("white")
        number.setSize(numSize)
        number.draw(win)
        for j in range(0, mapSize):
            if (i == 0): # Creates col numbers
                number = Text(Point(offset + j * pixelSize + pixelSize/2, int(offset/2) + 50), str(j + 1))
                number.setTextColor("white")
                number.setSize(numSize)
                number.draw(win)
                
            tile = Rectangle(Point(j * pixelSize + offset, i * pixelSize + 50 + offset), Point((j + 1) * pixelSize + offset, (i + 1) * pixelSize + 50 + offset))
            if (isinstance(worldMap[i][j], Ocean)):
                tile.setOutline("")
                tile.setFill("blue")
            else:
                tile.setWidth(2)
                tile.setFill("green")
            tile.draw(win)
    print("Successfully created a " + str(mapSize) + " x " + str(mapSize) + " map!")
    
# Spawns all civilization on random Plains tiles
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
#         ADD ALL CIVS TO ALLCIVS ARRAY
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= #
def spawnCivs():
    print("Preparing to spawn civilizations...")
    allCivs = [Ronin(), Slythe(), Bumbumopolis()] # <--------------
    for i in range(0, len(allCivs)):
        row = random.randint(1, mapSize - 1)
        col = random.randint(0, mapSize - 1)
        while (isinstance(worldMap[row][col], Ocean) and worldMap[row][col].getTaken() == True): # Finds a tile w/ Plains && is not taken
            row = random.randint(0, mapSize - 1)
            col = random.randint(0, mapSize - 1)
        worldMap[row][col].setTaken(True)
        worldMap[row][col].setOwner(allCivs[i])
        randomTile = Rectangle(Point(col * pixelSize + offset, row * pixelSize + 50 + offset), Point((col + 1) * pixelSize + offset, (row + 1) * pixelSize + 50 + offset))
        randomTile.setFill(allCivs[i].getColor())
        randomTile.draw(win)
        print("Spawned " + allCivs[i].getName() + " civilization at (" + str(col + 1) + ", " + str(row + 1) + ").")

# Central function of the program
def main():
    preGameSettings()
    calcPixelSize()
    global win
    win = GraphWin("Civilization Simulation",500,550)
    win.setBackground("black")

    header = Rectangle(Point(0,0), Point(500,50))
    header.setFill("white")
    header.draw(win)

    headerLine = Line(Point(0, 49), Point(500, 49))
    headerLine.draw(win)

    title = Text(Point(250, 25), "Civilization Simulation")
    title.draw(win)

    genWorldMap()
    spawnCivs()
main()
