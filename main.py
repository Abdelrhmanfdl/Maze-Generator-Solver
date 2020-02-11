import pygame, random, time
from collections import deque

def IfWantExit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

def defColors():
    global lightBlack, black, Watermelon, green, aqua, yellow
    lightBlack = (20 ,20 , 20)
    aqua = (0,255, 255)
    Watermelon = (200 , 130 , 123)
    green = (0 , 255 , 0)
    yellow = (255, 204, 0)

def initWindow(H , W):
    global width, height, sc

    width = W
    height = H
    pygame.init()
    sc = pygame.display.set_mode((width , height))
    pygame.display.set_caption("Fadl's MazeGenerator")
    # pygame.

def initGrid():

    for j in range(cellW, (cols+1)*cellW, cellW):
        for i in range(cellW, (rows+1)*cellW , cellW):
            pygame.draw.line(sc , lightBlack , (j,i) , (j,i+cellW ) )                                   #upR
            pygame.draw.line(sc , lightBlack , (j+cellW,i) , (j+cellW ,i+cellW) )             #downR
            pygame.draw.line(sc , lightBlack , (j,i) , (j+cellW, i) )                                 #leftUD
            pygame.draw.line(sc , lightBlack , (j,i+cellW) , (j+cellW , i+cellW) )             #rightUD
            pygame.display.update()

def carveDown(row , col):
    pygame.draw.rect(sc, Watermelon, (col*cellW+1, row*cellW+1, cellW-1, cellW*2-1), 0)
    pygame.display.update()
def carveUP(row , col):
    pygame.draw.rect(sc , Watermelon , (col*cellW+1, (row-1)*cellW+1, cellW-1, cellW*2-1), 0)
    pygame.display.update()
def carveRight(row , col):
    pygame.draw.rect(sc , Watermelon , (col*cellW+1, row*cellW+1, cellW*2-1, cellW-1), 0)
    pygame.display.update()
def carveLeft(row , col):
    pygame.draw.rect(sc , Watermelon , ((col-1)*cellW+1, row*cellW+1, cellW*2-1, cellW-1), 0)
    pygame.display.update()

def setColor(row , col, color):
    pygame.draw.rect(sc, color, (col*cellW+2, row*cellW+2, cellW-3, cellW-3), 0)
    pygame.display.update()

def pathStep(row, col, color):
    pygame.draw.rect(sc, yellow, (col*cellW+3, row*cellW+3, cellW-5, cellW-5), 0)
    pygame.display.update()

def buildMaze(R , C):
    global vis, gone
    vis=[ [0 for i in range(cols + 10)] for i in range(rows+10) ]
    gone = [ [0 for i in range(cols + 10)] for i in range(rows+10) ]

    for r in range(rows+10):
        for c in range(cols + 10):
            gone[r][c]= []

    stack = deque()
    stack.append((R , C))
    while len(stack) != 0:
        IfWantExit()
        # time.sleep(.1)
        (row, col) = stack.pop()

        setColor(row , col , green)

        vis[int(row)][int(col)] = 1
        directions = ['u', 'r', 'd', 'l']

        while len(directions) != 0:
            rand = random.choice(directions)
            directions.remove(rand)

            if rand == 'u':
                if (row-1) <= 0 or (row-1) > rows or vis[row-1][col] == 1:
                    continue
                else:
                    setColor(row , col , Watermelon)
                    carveUP(row, col)
                    gone[row][col].append('u')
                    gone[row-1][col].append('d')
                    stack.append((row, col))
                    stack.append((row-1, col))
                    break

            elif rand == 'r':
                if (col+1) > cols or (col+1) <= 0 or vis[row][col+1] == 1:
                    continue
                else:
                    setColor(row , col , Watermelon)
                    carveRight(row, col)
                    gone[row][col].append('r')
                    gone[row][col+1].append('l')
                    stack.append((row, col))
                    stack.append((row, col+1))
                    break

            elif rand == 'd':
                if (row+1) > rows or (row+1) <= 0 or vis[row+1][col] == 1:
                    continue
                else:
                    setColor(row , col , Watermelon)
                    carveDown(row, col)
                    gone[row][col].append('d')
                    gone[row+1][col].append('u')
                    stack.append((row, col))
                    stack.append((row+1, col))
                    break

            elif rand == 'l':
                if (col-1) <= 0 or (col-1) > cols or vis[row][col-1] == 1:
                    continue
                else:
                    setColor(row , col , Watermelon)
                    carveLeft(row, col)
                    gone[row][col].append('l')
                    gone[row][col-1].append('r')
                    stack.append((row, col))
                    stack.append((row, col-1))
                    break

        setColor(row , col , Watermelon)
    setColor(row , col , Watermelon)

def solve():
    found =  0

    memo = [ [0 for i in range(cols + 10)] for i in range(rows+10) ]

    for r in range(rows+10):
        for c in range(cols + 10):
            vis[r][c]= 0

    stack = deque()
    stack.append(start)

    while len(stack) > 0:
        IfWantExit()
        cur = stack.pop()
        if cur == end:
            found=1
            break
        vis[cur[0]][cur[1]] = 1
        for d in gone[cur[0]][cur[1]]:
            if d == 'u':
                gone[cur[0]][cur[1]][gone[cur[0]][cur[1]].index(d)] = 'X'
                if vis[cur[0]-1][cur[1]] == 0:
                    memo[cur[0]][cur[1]] = 'u'
                    stack.append(cur)
                    stack.append((cur[0]-1, cur[1]))
                    break
            elif d == 'd':
                gone[cur[0]][cur[1]][gone[cur[0]][cur[1]].index(d)] = 'X'
                if vis[cur[0]+1][cur[1]] == 0:
                    memo[cur[0]][cur[1]] = 'd'
                    stack.append(cur)
                    stack.append((cur[0]+1, cur[1]))
                    break
            elif d == 'r':
                gone[cur[0]][cur[1]][gone[cur[0]][cur[1]].index(d)] = 'X'
                if vis[cur[0]][cur[1]+1] == 0:
                    memo[cur[0]][cur[1]] = 'r'
                    stack.append(cur)
                    stack.append((cur[0], cur[1]+1))
                    break
            elif d == 'l':
                gone[cur[0]][cur[1]][gone[cur[0]][cur[1]].index(d)] = 'X'
                if vis[cur[0]][cur[1]-1] == 0:
                    memo[cur[0]][cur[1]] = 'l'
                    stack.append(cur)
                    stack.append((cur[0], cur[1]-1))
                    break

    cur = start
    while True:
        IfWantExit()
        time.sleep(.1)
        pathStep(cur[0], cur[1], aqua)
        if cur == end:
            break
        if memo[cur[0]][cur[1]] == 'u':
            cur = (cur[0]-1, cur[1])
        elif memo[cur[0]][cur[1]] == 'd':
            cur = (cur[0]+1, cur[1])
        elif memo[cur[0]][cur[1]] == 'r':
            cur = (cur[0], cur[1]+1)
        elif memo[cur[0]][cur[1]] == 'l':
            cur = (cur[0], cur[1]-1)

def main():
    global start, end, cols, rows, cellW

    cellW = 10
    rows = 49
    cols = 49

    start = (1, 1)
    end = (49, 49)

    defColors()
    initWindow(510, 510)
    initGrid()
    buildMaze(20, 20)
    pathStep(start[0], start[1], aqua)
    pathStep(end[0], end[1], aqua)
    solve()

main()

while True:
    IfWantExit()