import random
import sys
from queue import Queue

dx = [1,-1,0,0,1,-1,1,-1]
dy = [0,0,1,-1,1,-1,-1,1]

def can(i,j):
    return i < 8 and i > -1 and j < 8 and j > -1

def rules():
    print("\nto play the game you need to enter 1 letter and 2 numbers")
    print("ex: F23 -> cell 2 3 will be flaged")
    print("ex: U23 -> cell 2 3 will be unflaged")
    print("ex: D23 -> cell 2 3 will be daged\n")

def menu():
    print('\n','\t','-'*25)
    print("\t | welcom to minesweeper |")
    print('\t','-'*25,'\n\n')
    while True:
        print('1) play')
        print('2) rules')
        choice = int(input("enter you choice: "))
        if(choice == 1):
           play()
        elif(choice == 2):
           rules()
        else:
            sys.exit(0)

def set_empty_grid(val):
    grid = []
    for i in range(0,8):
        row = [val] * 8
        grid.append(row)
    return grid

def set_game_grid():
    new_grid = set_empty_grid(0)

    bombs = set()
    while len(bombs) < 10:
       x = random.randint(0,7)
       y = random.randint(0,7)
       bombs.add((x,y))

    for i in bombs:
       new_grid[i[0]][i[1]] = '*'

    for ind in bombs:
       for i in range(0,8):
           ni = ind[0] + dx[i]
           nj = ind[1] + dy[i]
           if can(ni,nj) and not (new_grid[ni][nj] == '*'):
               new_grid[ni][nj] += 1
    return new_grid

def print_grid(grid):
    print('  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8' ,end='')
    for i in range(0,8):
        print('\n','-'*33)
        print(i + 1,end= ' ')
        for j in range(0,8):
           print('|',grid[i][j] ,end= ' ')
    print('\n','-'*33)

def bfs(base_row,base_col,real_grid,fake_grid,visited):
    q = Queue()
    q.put((base_row,base_col))
    visited[base_row][base_col] = 1
    fake_grid[base_row][base_col] = real_grid[base_row][base_col]
    while(not q.empty()):
        parent_row, parent_col = q.get()
        for ind in range(0,8):
            neighbor_row = parent_row + dx[ind]
            neighbor_col = parent_col + dy[ind]
            if(can(neighbor_row,neighbor_col) and visited[neighbor_row][neighbor_col] == 0 and not real_grid[neighbor_row][neighbor_col] == '*'):
                fake_grid[neighbor_row][neighbor_col] = real_grid[neighbor_row][neighbor_col]
                if(real_grid[neighbor_row][neighbor_col] == 0):
                    q.put((neighbor_row,neighbor_col))
                    visited[neighbor_row][neighbor_col] = 1

def play():
    print('\n')
    #set all needed grids
    hidden_grid = set_game_grid()
    shown_grid = set_empty_grid('.')
    visited = set_empty_grid(0)

    #set bombs counter
    hidden_rem_bombs = 10
    shown_rem_bombs = 10
    while hidden_rem_bombs:
        print('The remaining bombs = ',shown_rem_bombs)
        print_grid(shown_grid)

        cell = input('enter action and cell: ')
        if not len(cell) == 3:
            continue
        x = int(cell[1]) - 1
        y = int(cell[2]) - 1
        if cell[0] not in 'FDU' or not can(x,y):
            continue

        if cell[0] == 'U':
            if(shown_grid[x][y] == 'F'):
                shown_grid[x][y] = '.'
                shown_rem_bombs += 1
                if(hidden_grid[x][y] == '*'):
                    hidden_rem_bombs += 1
        elif cell[0] == 'F':
            if(shown_grid[x][y] == '.'):
                shown_grid[x][y] = 'F'
                shown_rem_bombs -= 1
                if(hidden_grid[x][y] == '*'):
                    hidden_rem_bombs -= 1
        else:
            if(hidden_grid[x][y] == '*'):
                print('you are dead TT')
                print_grid(hidden_grid)
                print('\n')
                return
            elif(hidden_grid[x][y] == 0):
                bfs(x,y,hidden_grid,shown_grid,visited)
            else:
                shown_grid[x][y] = hidden_grid[x][y]

    print('you win !!!!!')
    print_grid(hidden_grid)
    print('\n')

        
menu()
