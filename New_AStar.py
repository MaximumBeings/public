"""
Original Board:
_____________________
🛣  ⛰  🛣  🛣  🛣  🛣
🛣  ⛰  🛣  🛣  🛣  🛣
🛣  ⛰  🛣  🛣  🛣  🛣
🛣  ⛰  🛣  🛣  🛣  🛣
🛣  🛣  🛣  🛣  ⛰  🛣

Solved Board:
______________
Start is cell [0, 0] and Goal is cell [0, 5]:
_____________________________________________
⚽  ⛰  🛣  🛣  🛣  🥅
🚚  ⛰  🛣  🛣  🚧  🚚
🚚  ⛰  🛣  🚧  🚧  🚚
🚚  ⛰  🚧  🚚  🚚  🚚
🚚  🚚  🚚  🚚  ⛰  🚧

Refactor of Udacity A* Search from C++
to Python

Program: Udacity C++ Nanodegree Program
IDE: CS50 IDE
"""



import pprint
import math

#board.txt
#https://github.com/MaximumBeings/public/blob/master/board.txt
"""
0,1,0,0,0,0,
0,1,0,0,0,0,
0,1,0,0,0,0,
0,1,0,0,0,0,
0,0,0,0,1,0,
"""

#directional Delta
delta = [[-1,0], [0,-1], [1,0],[0,1]]

global openList

class State:
    kEmpty = 0
    kObstacle = 1
    kClosed = 2
    kPath = 3
    kStart = 4
    kFinish = 5

def CellString(cell):
    if cell == State.kEmpty:
        return "🛣"
    elif cell == State.kObstacle:
        return "⛰"
    elif cell== State.kClosed:
        return "🚧"
    elif cell == State.kPath:
        return "🚚"
    elif cell == State.kStart:
        return "⚽"
    elif cell == State.kFinish:
        return "🥅"

def ReadBoardFile(fileName):
    result = []
    newResult = []
    res = []
    with open(fileName, "r") as f:
        for l in f:
            result.append(l.split())

    for x in result:
        temp = x[0].split()
        for y in temp[0][0:-1]:
            if y != ',':
                res.append(int(y))
        newResult.append(res)
        res = []
    return newResult

def PrintBoard(board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            print(CellString(board[x][y]), end="  ")
        print()

#Test RoadBoard

#board = ReadBoardFile("board.txt")
#pprint.pprint(board)
#PrintBoard(board)

def CheckValidCell(x, y, grid):
    on_grid_x = (x >= 0 and x < len(grid))
    on_grid_y = (y >= 0 and y < len(grid[0]))
    if (on_grid_x and on_grid_y):
        return grid[x][y] == State.kEmpty
    return False

#validCells = CheckValidCell(-1, 1, board)
#print(validCells)

def AddToOpen(x, y, g, h, openList, grid):
    openList.append([x,y,g,h])
    grid[x][y] = State.kClosed

"""
print()
print("openList Before Call AddToOpen")
print(openList)
print()
x = 3
y = 0
g = 5
h = 7
AddToOpen(x, y, g, 7, openList, board)
print("openList After Call AddToOpen")
print(openList)
print()
PrintBoard(board)
"""

def Heuristic(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def ExpandNeighbors(current, goal, openList, grid):
    x = current[0]
    y = current[1]
    g = current[2]

    for i in range(4):
        x2 = x + delta[i][0]
        y2 = y + delta[i][1]

        if (CheckValidCell(x2,y2, grid)):
            g2 = g + 1
            h2 = Heuristic(x2, y2, goal[0], goal[1])
            AddToOpen(x2, y2, g2, h2, openList, grid)

"""
print()
current = [3, 0, 5, 7]
goal = [5,5]
ExpandNeighbors(current, goal, openList, board)
print()
print(openList)
PrintBoard(board)
"""


def CellSort(v):
    v = sorted(v,key=lambda x: x[2]+x[3], reverse=True)
    return v
"""
print()
print(openList)
print()
openList = CellSort(openList)
print(openList)
"""

def Search(grid, init, goal):
    x = init[0]
    y = init[1]
    g = 0
    h = Heuristic(x, y, goal[0],goal[1])
    openList = []
    AddToOpen(x, y, g, h, openList, grid)

    while (len(openList) > 0):
        openList = CellSort(openList);

        current = openList.pop();
        #open.pop_back();
        x = current[0];
        y = current[1];
        grid[x][y] = State.kPath;

        #Check if we're done.
        if (x == goal[0] and y == goal[1]):
            grid[init[0]][init[1]] = State.kStart
            grid[goal[0]][goal[1]] = State.kFinish
            return grid

        ExpandNeighbors(current, goal, openList, grid)

    print("No Path Found")
    return []

if __name__ == '__main__':
    board = ReadBoardFile("board.txt")
    print()
    print("Original Board: ")
    print("_____________________")
    PrintBoard(board)
    print()

    init = [0,0]
    goal = [0,3]

    solution = Search(board, init, goal)
    print("Solved Board: ")
    print("______________")
    print(f"Start is cell {init} and Goal is cell {goal}: ")
    print("_____________________________________________")
    PrintBoard(solution)













