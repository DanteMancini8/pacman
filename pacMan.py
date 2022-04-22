from cmu_cs3_graphics import *
import math, random, copy

#this class will represent a graph as an adjacency dictionary. This was taken 
#from the mini-lecture on graphs
class Graph(object):
    def __init__(self):
        self.table = dict()
        
    #This method will add an edge between two nodes in a graph. This was taken 
    #from the mini-lecture on graphs
    def addEdge(self, nodeA, nodeB):
        # if either of the nodes is not already in the table, add them as keys 
        # to the table and set their values as empty sets
        if nodeA not in self.table:
            self.table[nodeA] = set()
        if nodeB not in self.table:
            self.table[nodeB] = set()
            
        #updating the table of edges by creating a two way edge between nodeA
        #and nodeB
        self.table[nodeA].add(nodeB)
        self.table[nodeB].add(nodeA)
        
    #This method will return the weight of an edge between nodeA and nodeB.
    #This was taken from the mini-lecture on graphs
    def getEdge(self, nodeA, nodeB):
        return self.table[nodeA][nodeB]
        
    # this method will return the table representing the nodes and edges that 
    # represent the pac man graph when the table is object is printed
    def __repr__(self):
        return f'{self.table}'
        
    #This method will return a list of all the nodes in the graph. This was 
    #taken from the mini-lecture on graphs
    def getNodes(self):
        return list(self.table)
        
    #This method will return a set of all the neighbor nodes of a given node
    #This was taken from the mini-lecture on graphs
    def getNeighbors(self, node):
        return set(self.table[node])
        
# this function will initialize the graph by adding all of the tuple (row,col)
# pairs as keys to the a dictionary and its values represent a set of (row,col)
# legal neighbors
def initializeGraph(app, size):
    # creating the varibale (drow, dcol) from a (row, col) to find all of the 
    # neighbors
    possibleNeighbors = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    # this will loop over all of the rows in the table based on the size
    for row in range(0, size):
        # this will loop over all of the cols in the table based on the size
        for col in range(0, size): 
            # this will loop over all of the possible neighbors that a 
            # (row, col) can have
            for drow, dcol in possibleNeighbors:
                # creating two variables to represent the (row, col) of the 
                # possible neighbor
                neighborRow, neighborCol = (row + drow, col + dcol)
                
                # calling isValidConnection to see if that it is possible to 
                # have a connection between the (row, col) and 
                # (neighborRow, neighborCol) based on the table dimensions
                if isValidConnection(neighborRow, neighborCol, size):
                    
                    #adding an edge to the graph
                    app.graph.addEdge((row, col), (neighborRow, neighborCol))
                    
# this method will return if there is a valid conenction between a (row, col) 
# and (neighborRow, neighborCol) is possible based on the board size
def isValidConnection(neighborRow, neighborCol, size):
    return (0 <= neighborRow < size) and (0 <= neighborCol < size)
                
                
# primsAlgorithm will randomly generate connections between nodes. Those nodes
# that are missing connections to their possible, legal neighbors will have a 
# wall drawn in between 
# used https://www.programiz.com/dsa/prim-algorithm for help
def primsAlgorithm(app, size):
    #initiatialing a new Graph to represent the output
    randomizedGraph = Graph()
    
    #randomly generate a starting cell within the maze
    (startRow, startCol) = (random.randrange(0, size), random.randrange(0,size))
    
    #generate a set of all unvisited neighbors
    unvisitedNodes = set()
    
    #generating a set of all the nodes that have been seen 
    seen = set()
    
    # this method will initially add all of the neighbors of the random
    # (startRow, startCol) into the unvisitedNodes set
    for row, col in app.graph.getNeighbors((startRow, startCol)):
        unvisitedNodes.add((row, col))
    
    # adding the (startRow, startCol) into the seen set    
    seen.add((startRow, startCol))
    
    # this loop will continue until all of the possible nodes have been seen
    while(len(seen) != size ** 2):
        
        # randomly choosing a (row, col) from the unvisitedList of Nodes
        unvisitedRow, unvisitedCol = random.choice(list(unvisitedNodes))
        
        # creating the list possibilities to list all of the possible nodes that 
        # can form an edge with (unvisitedRow, unvisitedCol)
        possibilities = []
        
        # this will loop over all of the (row, col) that have been seen 
        for (row, col) in seen: 
            # (row, col) will be added to the possibilities list if it can form 
            # an edge with (unvistedRow, unvisitedCol)
            if (unvisitedRow, unvisitedCol) in app.graph.table[(row,col)]:
                possibilities.append((row, col))

        # randomly form an edge between a random node that can form an edge 
        # with (unvisitedRow, unvisitedCol)
        randomizedGraph.addEdge(random.choice(possibilities), 
                                (unvisitedRow, unvisitedCol))
                
        # this will loop over all of the nodes that are neighbors with 
        # (unvisitedRow, unvisitedCol)
        for row, col in app.graph.getNeighbors((unvisitedRow, unvisitedCol)):
            
            # the neighbor of (row, col) will be added to unvsited Nodes if it 
            # has not been seen already 
            if(row, col) not in seen:
                unvisitedNodes.add((row, col))
                    
        # adding the (unvisitedRow, unvisitedCol) to seen after it has been seen 
        seen.add(((unvisitedRow, unvisitedCol)))
        
        # removing the (unvisitedRow, unvisitedCol) from unvisitedNodes after 
        # it has been visited
        unvisitedNodes.remove((unvisitedRow, unvisitedCol))

    return randomizedGraph
    
# this function will make the top half of the graph symnmetrical across the 
# y - axis and the bottom half of the graph symmetrical across the y - axis 
#THIS FUNCTION MAY NOT BE USED IN THE FINAL PROJECT, SO IT IS NOT COMMENTED
def makeSymmetrical(app, size):
    for row in range (0, size//2):
        for col in range(0, size//2):
            neighbors = app.pacManGraph.getNeighbors((row, col))
            symRow, symCol = (row, (size - 1 - col))
            symNeighbors = set()

            for neighRow, neighCol in neighbors:
                symNeighbors.add((neighRow, (size - 1 - neighCol)))
                
            app.pacManGraph.table[(symRow, symCol)] = symNeighbors
            
    for row in range (size//2, size):
        for col in range(size//2, size):
            neighbors = app.pacManGraph.getNeighbors((row, col))
            symRow, symCol = (row, (size - 1 - col))
            symNeighbors = set()

            for neighRow, neighCol in neighbors:
                symNeighbors.add((neighRow, (size - 1 - neighCol)))
                


            app.pacManGraph.table[(symRow, symCol)] = symNeighbors
        
        
## all of the stuff Below this will have to do with the movement of enemies 
class Enemies(object):
    #creating the class variable eatable, to represent whether the enemies are
    # eatable by the pacMan color or not
    eatable = False
    
    def __init__(self, color):
        # if the enemies become eatable, we want to switch all of the colors of 
        # the enemy to medium blue
        if Enemies.eatable:
            self.color = 'mediumBlue'
        else:
            self.color = color
            
        # randomly selecting a starting location on the bottom half of the 
        # pacMan board
        self.cx = random.randrange(5, 10)
        self.cy = random.randrange(5, 10)

        
#this class will initialize 5 enemies of different colors
def createEnemies(app):
    #creating a list of colors that the pacMan enemies will take upon
    colors = ['red', 'cyan', 'green', 'pink', 'orange']
    
    # creating a list to contain the Enemies objects that are created
    enemyList = []
    
    # this will loop over the number of enemies, which happens to be equal to 
    # the length of the colors list 
    for i in range(app.numEnemies):
        enemyColor = colors[i]
        enemyList.append(Enemies(enemyColor))

    return enemyList



# used https://www.youtube.com/watch?v=Ub4-nG09PFw  for reference when 
# writing the algorithm for dijkstras. Since the graph representing the board 
# uses unweighted edges, the only cost that matters is the heuristic function 
# that is represented in the algorithm by the manhattan distance
def dijkstrasAlgorithm(app, start, goal):
    # creating a dictionary to record the cost to reach to that node, this will 
    # be updated as we move through the graph
    shortest_distance = dict() 
    
    # this will keep track of the path that has led us to this node
    track_predecessor = dict()
    
    # creating a local variable to represent the graph 
    unseenNodes = copy.deepcopy(app.graph.table)
    
    # creating a very large number to represent the cost of the node 
    infinity = 999999
    
    # going to trace the optimal journey back to the start not
    path = []
    
    # setting up the shortest distance dictionary by setting the cost of each of
    # of the nodes equal to infinity
    for node in unseenNodes:
        shortest_distance[node] = infinity
        
    # setting the start node cost = 0
    shortest_distance[start] = 0
    
    # this will loop over the unseen nodes and sto ponce all the nodes have been
    # seen 
    while unseenNodes:
        # creating a local variable to represent the node with the minimum
        # distance
        min_distance_node = None

        # looping through all of the nodes to find the node whos cost is the 
        # least
        for node in unseenNodes:
            #setting the min_distance_node = firstNode originally
            if min_distance_node == None:
                min_distance_node = node
            # comparing the cost of the node to the min_distance_node to see 
            # if its cost is lower
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node
                
        #getting the neighbors from the minimum_distance_node to start forming 
        # the path   
        path_options = app.pacManGraph.getNeighbors(min_distance_node)
        
        # this will loop over all of the edges that the min_distance_node is 
        # connected to 
        for neighbor_node in path_options:
            # calling manhattan Distance to represent the heuristic part of the 
            # A* Algorithm, which solves for the manhattan distance between the
            # a node and the pacMan character
            distance = manhattanDistance(app, neighbor_node)
            
            # if manhattan distance + distance it took to get to the 
            # min_distance node is less than the current cost of the neighbor
            # node, we want to update the cost of the neighbor node to be the
            # sum of the manhattan distance + the cost it took to get to the 
            # current node
            if (distance + shortest_distance[min_distance_node] < 
                    shortest_distance[neighbor_node]):
                shortest_distance[neighbor_node] = (shortest_distance[min_distance_node]
                                                    + distance)
                                                    
                # to keep track of the order in which we viewed the nodes, we
                # set the key in track_predecessor = min_distance node to 
                # remember that we saw the min_distance node before the 
                # neighbor node
                track_predecessor[neighbor_node] = min_distance_node
                
        # once we have visited the min_distance_node, we want to remove it from 
        # the list of unseen nodes
        unseenNodes.pop(min_distance_node)

    # creating a back tracking algorithm to create the path of least cost to 
    # reach pacMan
    # we want to create a local variable currentNode and set it equal to the 
    # goal, which will be the location of the pacMan character
    currentNode = goal

    #this will loop until the current node is equal to the start node
    while currentNode != start:
        # using a try except statement hear to avoid crashing if the pacMan 
        # character is not reachable for any reason
        try:
            # if it is reachabkle, we want to insert the current node at the 0
            # index in the path list, and then set the currentNode equal to its
            # value in the track_predecessor dictionary
            path.insert(0, currentNode)
            currentNode = track_predecessor[currentNode]
        except:
            # if the path is not reachable, we want to break
            print("Path is not reachable")
            break

    # inserting our current position currently at the 0th index in the path list
    path.insert(0, start)

    if shortest_distance[currentNode] != infinity:
        # we will return the path
        return path
    
# this function will move the enemy based on the dijkstras algorthm
def moveEnemy(app):
    # this will loop over all of the enemy objects created and stored in 
    # app.enemies
    for enemy in app.enemies:
        # calling dijstrasAlgorithm to find the shortest path between the 
        # current enemy position and the current pacManPos. A list of the 
        # (row, cols) needed to get to pacMan will be displayed 
        path = dijkstrasAlgorithm(app, (enemy.cx, enemy.cy), app.pacManPos)
        
        # since the path return starts with the current position of the enemy 
        # object, the (row, col) at index 1 will represent the next space that 
        # the enemy has to move to in order to reach the pacMan character
        nextRow, nextCol = path[1]
        
        
        # setting the cx, cy of the enemy equal to the nextRow, nextCol 
        # determined by dijkstras algorithm
        enemy.cx, enemy.cy = nextRow, nextCol
            
#this method will check to see if any of the enemies intersect pacMan
def enemyIntersectPacMan(app):
    #this will loop over all of the enemies stored in app.enemies
    for enemy in app.enemies:
        # if the pacManPos and the enemyPos are the same and the enemies are not
        # eatable, then app.gameOver = True
        if app.pacManPos == (enemy.cx, enemy.cy) and Enemies.eatable == False:
            app.gameOver = True
            return
        # else, if the enemies are eatable, then we want to remove the enemy that
        # was just eaten by pacMan and spawn a new enemy of the same color of 
        # the one that was just eaten
        elif app.pacManPos == (enemy.cx, enemy.cy) and Enemies.eatable == True:
            color = enemy.color
            app.enemies.remove(enemy)
            app.enemies.append(Enemy(color))
            
# onStep will move the enemies and check to see if there are any intersections 
# with the pacMan character
def onStep(app):
    # if the game is over, do not call onStep to do anything and just leave
    # the function
    if app.gameOver:
        return
    
    # calling moveEnemy to move the enemy towards the pacMan character
    moveEnemy(app)
    
    # calling enemyIntersectPacMan to check to see if pacMan and the enemy have
    # intersected
    enemyIntersectPacMan(app)
    
    # increasing pacManCounter by 2 and modding it by 4 to adjust the size of 
    # pacMan's mouth on every step so it looks like it is moving
    app.pacManCounter = (app.pacManCounter + 2) % 4
    
# this function will compute the manhattan distance between an enemy and pacMan
def manhattanDistance(app, node):
    return (abs(node[0] - app.pacManPos[0]) + abs(node[1] - app.pacManPos[1]))
    
#this function will draw the enemies on the map
def drawEnemies(app):
    for enemy in app.enemies:
        #getting the top left position of a particular cell based on the dots 
        #current position, given by app.dotPos
        left, top, cellWidth, cellHeight = getCellBounds(app,enemy.cx,enemy.cy)
                                                
        #calculating the center coordinates of the dot inside of the grid                                           
        cx = left + cellWidth // 2
        cy = top + cellHeight // 2
    
        drawCircle(cx, cy, 15, fill = enemy.color)
        
        
## EVERYTHING BELOW HERE WILL BE FOR THE COINS ##
class Coin(object):
    centers = set()
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy
        self.radius = 5
        self.color = 'gold'
        Coin.centers.add((cx, cy))
        

# this function will create Coins on the map        
def createCoins(app):
    # creating a set of all of the possible node locations on the board
    possibleSpots = set(node for node in app.graph.table)
    
    # we don't want a coin that is already sitting on top of Pac Man
    possibleSpots.remove(app.pacManPos)
    
    # creating a list to store the coin objects
    coinLocations = []
    
    # this will loop over the number of coins that we want to put on the map
    for _ in range(app.numCoins):
        #randomly choising to put a coin at a certain node on the map
        (row, col) = random.choice(list(possibleSpots))
        
        # creating a Coin object based on the (row, col) just found and it
        # appending it to the coinLocations list
        coinLocations.append(Coin(row, col))
        
        # removing the (row, col) from the list of possible locations since it 
        # already has a coin there
        possibleSpots.remove((row, col))
        
    return coinLocations
    
# this function will draw all of the coins and the special coins at there
# specific location
def drawCoinsAndSpecialCoins(app):
    #this will loop over all of the coin objects in app.coins
    for coin in app.coins:
        # getting the top left position of a particular cell based on the dots 
        # current position, given by app.dotPos
        left, top, cellWidth, cellHeight = getCellBounds(app, coin.cx, coin.cy)
        
        # calculating the center coordinates of the dot inside of the grid 
        cx = left + cellWidth // 2
        cy = top + cellHeight // 2
        
        # calling draw circle: the coins will be represented as circles
        drawCircle(cx, cy, coin.radius, fill = coin.color)
    
    #this will loop over all of the special coin objects in app.coins
    for specialCoin in app.specialCoins:
        #getting the top left position of a particular cell based on the dots 
        #current position, given by app.dotPos
        left, top, cellWidth, cellHeight = getCellBounds(app, specialCoin.cx, 
                                                            specialCoin.cy)
                                                            
        #calculating the center coordinates of the dot inside of the grid 
        cx = left + cellWidth // 2
        cy = top + cellHeight // 2
        
        # calling draw circle: the specialCoins will be represented as circles
        drawCircle(cx, cy, specialCoin.radius, fill = specialCoin.color)
    
#creating the class SpecialCoin that will be a subclass of Coin
class SpecialCoin(Coin):
    centers = set()
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.radius = 10
        self.color = 'lightSalmon'
        SpecialCoin.centers.add((cx, cy))
        
# this function will find the locations that specialCoins can be placed and then 
# create specialCoin objects at those locations
def createSpecialCoins(app):
    #creating a set of all the possible nodes in the board
    possibleSpots = set(node for node in app.graph.table)
    
    #creating a set to represent the taken positions
    takenPositions = set()
    
    #adding the pacMan starting location to the set of takenPositions
    takenPositions.add(app.pacManPos)
    
    # this will loop through all of the enemies in app.enemies and add them 
    # their respective cx, cy position to the set
    for enemy in app.enemies:
        takenPositions.add((enemy.cx, enemy.cy))
        
    
    # this will loop through all of the coins in app.coins and add them 
    # their respective cx, cy position to the set
    for coin in app.coins:
        takenPositions.add((coin.cx, coin.cy))
    
    # this will loop over all of the possible nodes on the board and remove the 
    # ones that are already taken 
    for node in possibleSpots:
        if (node in takenPositions):
            possibleSpots.remove(node)
            
    # creating a list for the specialCoinLocations
    specialCoinLocations = []
    
    # this will loop over the number of special coins that we want to have 
    # initially
    for _ in range(app.numSpecialCoins):
        #randomly choosing a cx, cy from the possibleSpots and creating a 
        # specialCoin object at that location
        cx, cy = random.choice(list(possibleSpots))
        specialCoinLocations.append(SpecialCoin(cx, cy))
        
    return specialCoinLocations
        
#onAppStart will set the initial parameters for the graphics
def onAppStart(app):
    #Pac-Man variables
    app.pacManPos = (0,0)
    app.pacManR = 20
    app.pacManColor = 'yellow'
    app.pacManCounter = 0.1
    app.dRow, app.dCol = 0,0
            
    
    #Enemy Variables
    app.numEnemies = 5
    app.enemies = createEnemies(app)
    
    #Maze Variables
    app.rows = app.cols = 10
    app.margin = 20
    app.graph = Graph()
    initializeGraph(app, size = 10)
    app.pacManGraph = primsAlgorithm(app, size = 10)
    #makeSymmetrical(app, size = 10)
    
    #Coin Variables
    app.numCoins = 86
    app.numSpecialCoins = 4
    app.coins = createCoins(app)
    app.specialCoins = createSpecialCoins(app)
    
    #Game variables
    app.score = 0
    app.gameOver = False

# this function will allow the user to use the 'up', 'down', 'right', and 'left'
# keys in order to move the PacMan character
def onKeyPress(app, key):
    # only allow user input if the game is not over, besides if they want to 
    # restart the game
    if app.gameOver:
        #if the 'r' key is pressed, call onAppStart to restart the app
        if key == 'r':
            onAppStart(app)
        else:
            # if anything but 'r' is called when the game is over, it will not 
            # change anything
            return
    drow, dcol = 0,0
    # if the user presses 'up', subtract 1 from drow
    if key == 'up':
        drow -= 1
        
    # if the user presses 'down', add 1 from drow
    elif key == 'down':
        drow += 1
        
    #if the user presses 'left', subtract 1 from dcol 
    elif key == 'left':
        dcol -= 1
        
    #if the user presses 'right', add 1 from dcol
    elif key == 'right':
        dcol += 1
        
    app.dRow, app.dCol = drow, dcol
    #call move to move pacMan based on the user's key press
    return move(app, drow, dcol)
    
# this function will change the PacMan Parameters based on whether or not the 
# move is Legal
def move(app, drow, dcol):
    
    # unpack the currRow and currCol of pacMan
    currRow, currCol = app.pacManPos
    
    # compute the nextRow and nextCol based on the drow, dcol
    nextRow, nextCol = currRow + drow, currCol + dcol
    
    # calling isLegalMove to check if pacMan can move into the (row, col)
    if isLegalMove(app, currRow, currCol, nextRow, nextCol):
        app.pacManPos = (nextRow, nextCol)
        anyCoinsGathered(app)
        
# this function will check if the location where pacMan moved to has any coins
# if it does, it will remove the coin
def anyCoinsGathered(app):
    # this will loop through all of the coins in app.coins
    for coin in app.coins:
        # if the current pacManPos == the (row, col) location of the coin, we
        # want to remove the coin from the list of coins
        if app.pacManPos == (coin.cx, coin.cy):
            app.coins.remove(coin)
            # return here since there can only be one coin or specialCoin per 
            # (row, col) location
            app.score += 10
            return
        
    # this will loop through all of the speicalCoins in app.specialCoins
    for specialCoin in app.specialCoins:
        # if the current pacManPos == the (row, col) location of the specialCoin
        # we want to remove the special coin from the list of special coins
        if app.pacManPos == (specialCoin.cx, specialCoin.cy):
            app.specialCoins.remove(specialCoin)
            # return here since there can only be one coin or specialCoin per 
            # (row, col) location
            app.score += 50
            Enemies.eatable = True
            return
        
# this function will check to see if the PacMan character is able to move to 
# another node. This will check the dictionary representing the nodes and their
# respective edges to see if an edge exists between (currRow, currCol) and 
# (nextRow, nextCol)
def isLegalMove(app, currRow, currCol, nextRow, nextCol):
    return (nextRow, nextCol) in app.pacManGraph.table[(currRow, currCol)]
    

# this code was taken from the 112 course website. this will convert the 
# (row, col) to coordinates on the canvas 
# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
def getCellBounds(app, row, col):
    # calculating the grid width and the grid height after subtracting the 
    # margins on the respective sides of the grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    
    # calculating the width and height of a single cell based on the 
    # gridWidth and gridHeight previously calculated
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    
    # computing the x and y coordinate of the top left corner of the cell
    x0 = app.margin + cellWidth * col
    y0 = app.margin + cellHeight * row
    return (x0, y0, cellWidth, cellHeight)
    

def drawWalls(app):
    for (row, col) in app.pacManGraph.table:
        for connection in app.graph.table[(row, col)]:
            if connection not in app.pacManGraph.table[(row, col)]:
                connectRow, connectCol = connection
                #what to do if the wall is between two squares in the same row
                if connectRow == row and col > connectCol:
                    (x0, y0, cellWidth, cellHeight) = getCellBounds(app, row, col)
                    drawLine(x0, y0, x0, y0 + cellHeight, fill = 'mediumBlue')
                elif connectRow == row and connectCol > col:
                    (x0, y0, cellWidth, cellHeight) = getCellBounds(app, 
                                                        connectRow, connectCol)
                    drawLine(x0, y0, x0, y0 + cellHeight, fill = 'mediumBlue')
                #what to do if the wall is between two squares in the same col
                elif connectCol == col and row > connectRow:
                    (x0, y0, cellWidth, cellHeight) = getCellBounds(app, row, col)
                    drawLine(x0, y0, x0 + cellWidth, y0, fill = 'mediumBlue')
                elif connectCol == col and connectRow > row:
                    (x0, y0, cellWidth, cellHeight) = getCellBounds(app, 
                                                        connectRow, connectCol)
                    drawLine(x0, y0, x0 + cellWidth, y0, fill = 'mediumBlue')
                    
def drawPacMan(app):
    #getting the top left position of a particular cell based on the dots 
    #current position, given by app.pacManPos
    left, top, cellWidth, cellHeight = getCellBounds(app, app.pacManPos[0],
                                                        app.pacManPos[1])
                                                
    #calculating the center coordinates of the dot inside of the grid                                           
    cx = left + cellWidth // 2
    cy = top + cellHeight // 2
    
    # creating variables for the mouth of pacMan, which will be drawn as a 
    # triangle
    # angle will represent the rotation of the triangle that needs to 
    # be drawn dpending on which direction pacMan is going
    angle = 0
    
    # triangleCx and triangleCy will represent the cx, cy coordinates of the 
    # traignle. one of these values will always be adjusted depending on which 
    # way pack man is traveling
    triangleCx, triangleCy = cx, cy
    
    #if app.dRow, app.dCol = (1,0) then pacMan is moving down 
    if (app.dRow, app.dCol) == (1,0): 
        # offset the cy value of the triangle by 20 so it looks like a mouth
        # if pacMan is traveling down, there is no reason to alter the angle
        triangleCy += 20
        
    #if app.dRow, app.dCol = (-1,0) then pacMan is moving up 
    elif (app.dRow, app.dCol) == (-1,0): 
        #offset the cy value of the triangle by 20 so it looks like a mouth
        # if pacMan is traveling up, we need to rotate the triangle by 180
        angle = 180
        triangleCy -= 20
        
    #if app.dRow, app.dCol = (0,1) then pacMan is moving to the right 
    elif (app.dRow, app.dCol) == (0, 1) or (app.dRow, app.dCol) == (0,0): 
        # offset the cx value of the triangle by 20 so it looks like a mouth
        # if pacMan is traveling to the right, we need to rotate the triangle by
        # 270 degrees
        angle = 270
        triangleCx += 20
    #if app.dRow, app.dCol = (0,1) then pacMan is moving to the left 
    elif (app.dRow, app.dCol) == (0, -1):
        # offset the cx value of the triangle by 20 so it looks like a mouth
        # if pacMan is traveling to the left, we need to rotate the triangle by
        # 90 degrees
        angle = 90
        triangleCx -= 20
        
    
    #trawing a circle to represent the body of the pack man 
    drawCircle(cx, cy, app.pacManR - 5, fill = app.pacManColor)
    
    #drawing the mouth of bac man as a triangle that is off set
    #pacManCounter will change the size of the triangle every time onStep is 
    #called so that it looks like pacMan is eating the coins
    drawRegularPolygon(triangleCx, triangleCy, 
                        #off setting the center radius of the polygon
                        app.pacManCounter*(cellWidth//3),
                        3, #the number of points in a triable
                        rotateAngle = angle)
    
# this app will draw the output when an enemy intersects the pacMan character
# which indicates that the game is over
def drawGameOver(app):
    #drawing the Game Over label
    drawLabel('Game Over!', app.width // 2, app.height //2, size = 24, 
                bold = True, italic = True)
                
    #outputting the score that the user scored during the game
    drawLabel(f'Score: {app.score}', app.width // 2, app.height // 2 + 25)
    
    #drawing the directions if they wanted to play again
    drawLabel("To Play Again: press 'r'", app.width // 2, app.height // 2 + 50)
    
#this function will draw the current score of the game in the bottom left hand
#corner of the screen
def drawScore(app):
    #calling drawLabel to draw the score in the bottom left corner of the canvas
    drawLabel(f'Score: {app.score}', 0, app.height, align = 'left-bottom', 
                fill = 'white')
    
#this function will redraw all of the components of the pacMan game
def redrawAll(app):
    # if the game is over, it will display a message saying the score of the 
    # game and how to restart if you want to play again
    if app.gameOver:
        drawGameOver(app)
    else:
        #calling draw Rect to make the background of the game black
        drawRect(0,0, app.width, app.height, fill = 'black')
        
        #calling the rest of the components of the pacMan game to be drawn
        drawPacMan(app)
        drawWalls(app)
        drawCoinsAndSpecialCoins(app)
        drawEnemies(app)
        drawScore(app)

    

def main():
    runApp(width=400, height=400)

main()
