import pygame
import random
import time
from sortedcontainers import SortedSet

# Initialize Pygame
pygame.init()

# Set up the screen width and size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Solving mazes with obstacles")  #caption

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Constants to dscribe the indicators
obstacle = 3
trackPath = 4
solvedRoute = 5
startEnd=6

# Constants
CELL_SIZE = 20
ROWS = SCREEN_HEIGHT // CELL_SIZE
COLS = SCREEN_WIDTH // CELL_SIZE

imp_boxes=[(0,0),(ROWS-1,COLS-1),(ROWS-2,COLS-1),(0,1),(1,0),(ROWS-1,COLS-2),(2,0)]  #imp squares that should not be obstacles for better maze generation,any modification can be done.


# Function to generate random obstacles
def generate_obstacles():
    obstacles =set()
    while len(obstacles) < 400:  # Adjust the number of obstacles as needed
        obs=(random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
        if obs not in imp_boxes:  # Ensure the start and end cell is not an obstacle
            obstacles.add(obs)
    return obstacles


# Function to create a maze 2D array
def create_maze():
    maze = [[0] * COLS for _ in range(ROWS)]
    obstacles = generate_obstacles()
    for obs in obstacles:
        maze[obs[0]][obs[1]] = obstacle
    return maze


# Function to draw the maze on the screen
def draw_maze(maze):
    for y in range(ROWS):
        for x in range(COLS):
            if maze[y][x]==obstacle:
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x]==trackPath:
                pygame.draw.rect(screen,WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif maze[y][x]==solvedRoute:
                pygame.draw.rect(screen, GREEN, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# Manhattan distance heuristic
def heuristic(point,end):
    return abs(point[0]-end[0])+abs(point[1]-end[1])


# Getting the neighbours
def neighbours(current,maze):
    row,col=current[0],current[1]
    for dx,dy in [[-1,0],[0,-1],[1,0],[0,1]]:
        nextRow=dx+row
        nextCol=dy+col
        if nextCol>=0 and nextCol<COLS and nextRow>=0 and nextRow<ROWS and maze[nextRow][nextCol]!=obstacle:
            yield (nextRow,nextCol)  #returning an iterator or generator function


# Function to run the algorithm
def solver_algorithm(maze):   #by default A* algorithm, but we can modify it to djikstra
    start = (0,0)
    end = (ROWS-1,COLS-1)

    pq=SortedSet()
    pq.add((heuristic(start, end), start))
    path={}
    g_score={start: 0}

    while pq:
        _, current=pq.pop(0)

        maze[current[0]][current[1]]=trackPath

        screen.fill(BLACK)
        draw_maze(maze)
        pygame.display.flip()
        time.sleep(0.01)

        if current==end:
            finalPath=[]
            while current in path:
                finalPath.append(current)
                current=path.get(current)
            finalPath.append(start)
            finalPath.reverse()
            return finalPath

        for neighbour in neighbours(current, maze):
            current_G_score=g_score.get(current,float('inf'))
            updated_G_score=current_G_score + 1

            if updated_G_score<g_score.get(neighbour,float('inf')):
                path[neighbour]=current
                g_score[neighbour]=updated_G_score
                f_score = updated_G_score+heuristic(neighbour, end)
                pq.add((f_score, neighbour))  # We can also see the performance of djikstra by using updated_G_score inplace of f_score in the add method

    return None


# Main function
def main():
    # Creating the initial maze
    maze=create_maze()

    # Displaying the initial maze
    screen.fill(BLACK)
    draw_maze(maze)
    pygame.display.flip()

    # Running the algorithm to find the solution path
    finalList=solver_algorithm(maze)

    # Updating the maze with the solution path
    if finalList:
        for row, col in finalList:
            maze[row][col]=solvedRoute

    # Drawing the maze with the solution path
    screen.fill(BLACK)
    draw_maze(maze)
    pygame.display.flip()

    # Game loop
    running=True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

    # Quiting Pygame when we want
    pygame.quit()

# Call the main executable function
main()
