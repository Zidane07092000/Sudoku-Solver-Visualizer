from re import T
import pygame
import requests
 
# initialise the pygame font
pygame.init()
pygame.font.init()
 

WIDTH,HEIGHT =700,600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #Size of Screen

response=requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
 
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(0, 153, 153)
YELLOW=(255,255,0)
RED=(255,0,0)

pygame.display.set_caption("SUDOKU SOLVER USING BACKTRACKING") #Title Name
 
x = 0
y = 0
dif = 60
val = 0
# Default Sudoku Board.
board = response.json()['board']
board_original = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
board_writing = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
board_solved = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 20)

 


def isValid(board,row,col,n):
    for i in range(9):
        if (board[i][col]==n or board[row][i]==n):
            return False
    currRow=row-row%3
    currCol=col-col%3
    for i in range(3):
        for j in range(3):
            if(board[currRow+i][currCol+j]==n):
                return False
    return True

def solve(row,col):
    if row==9:
        return True
    nextRow,nextRow=-1,-1
    if col==8:
        nextCol=0
        nextRow=row+1
    else:
        nextCol=col+1
        nextRow=row
    if board_solved[row][col]==0:
        for i in range(1,10):
            if isValid(board_solved,row,col,i):
                board_solved[row][col]=i
                if solve(nextRow,nextCol):
                    return True
                board_solved[row][col]=0
    else:
        return solve(nextRow,nextCol)


def Solver(row,col):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if row==9:
        return True
    nextRow,nextRow=-1,-1
    if col==8:
        nextCol=0
        nextRow=row+1
    else:
        nextCol=col+1
        nextRow=row
    pygame.event.pump() 
    if board[row][col]==0:
        for i in range(1,10):
            if isValid(board,row,col,i):
                board[row][col]=i
                write(row,col,i)
                if Solver(nextRow,nextCol):
                    return True
                board[row][col]=0
                write(row,col,0)
    else:
        return Solver(nextRow,nextCol)

def check(x, y):
    print(x,y)
    if board_solved[x][y]==board_writing[x][y]:
        return True
    return False

def Reset():
   
    for i in range (9):
        for j in range (9):
            if board_original[i][j]== 0:
                pygame.draw.rect(SCREEN, WHITE, (j * dif, i * dif, dif , dif )) 
                board[i][j]=board_original[i][j]
                board_writing[i][j]=board_original[j][j]
    draw_border() 
    pygame.display.update() 


def draw():
    # Draw the lines
    SCREEN.fill(WHITE)
    
    pygame.draw.rect(SCREEN,RED,(560,30,100,60))
    Start_button = font2.render("SOLVE", True, BLACK)
    SCREEN.blit(Start_button, (562,30))
    pygame.draw.rect(SCREEN,RED,(560,180,100,60))
    Reset_button = font2.render("RESET", True, BLACK)
    SCREEN.blit(Reset_button, (562,180))
    for i in range (9):
        for j in range (9):
            if board[i][j]!= 0:
 
                pygame.draw.rect(SCREEN, BLUE, (j * dif, i * dif, dif , dif ))
                INITIAL_NUMBER = font1.render(str(board[i][j]), True, BLACK)
                SCREEN.blit(INITIAL_NUMBER, (j * dif+15, i * dif))
            else:
                pygame.draw.rect(SCREEN, WHITE, (j * dif, i * dif, dif , dif ))        
    draw_border() 
    pygame.display.update()  
 
 
def insert(position):
    x,y=position[1]//60,position[0]//60
    run=False
    if (x>=0 and x<9 and y>=0 and y<9 and board_original[x][y]==0):
        run=True
    while run:
        pygame.draw.rect(SCREEN, RED, (y*dif, x*dif, dif, dif),  2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if board_original[x][y]!=0:
                    return
                if (event.key==48):
                    board_writing[x][y]=event.key-48
                    pygame.draw.rect(SCREEN,WHITE,(y*dif,x*dif,dif,dif))
                    draw_border()
                    pygame.display.update()
                    # return
                if (0<event.key-48<10):
                    board_writing[x][y]=event.key-48
                    pygame.draw.rect(SCREEN,WHITE,(y*dif,x*dif,dif,dif))
                    NEW_NUMBER = font1.render(str(event.key-48), True, BLACK)
                    SCREEN.blit(NEW_NUMBER, (y * dif+15, x * dif))
                   
                    draw_border()
                    pygame.display.update()
                    # return
                if (event.key==pygame.K_c):
                    if check(x,y):
                        pygame.draw.rect(SCREEN, YELLOW, (y*dif, x*dif, dif, dif))
                        NEW_NUMBER = font1.render(str(board_solved[x][y]), True, BLACK)
                        SCREEN.blit(NEW_NUMBER, (y * dif+15, x * dif))
                        board[x][y]=board_solved[x][y]
                        draw_border()
                        pygame.display.update()
                        run=False
                        return
                    else:
                        board_writing[x][y]=0
                        pygame.draw.rect(SCREEN, WHITE, (y*dif, x*dif, dif, dif))
                        draw_border()
                        pygame.display.update()
                        run=False
                        return

                if event.key==pygame.K_RETURN:
                    pygame.draw.rect(SCREEN, WHITE, (y*dif, x*dif, dif, dif),  2)
                    draw_border()
                    pygame.display.update()
                    run=False
                    return
                # return
    return


 
# # Solves the sudoku board using Backtracking Algorithm
def draw_border():
    for k in range(10):
        if k % 3 == 0 :
            thick = 7
        else:
            thick = 1
        pygame.draw.line(SCREEN, BLACK, (0, k * dif), (540, k * dif), thick)
        pygame.draw.line(SCREEN, BLACK, (k * dif, 0), (k * dif, 540), thick) 
    
def write(i,j,val):
    pygame.time.delay(10)
    if (val>0):
        pygame.draw.rect(SCREEN, YELLOW, (j * dif, i * dif, dif , dif ))
        NEW_NUMBER = font1.render(str(val), True, BLACK)
        SCREEN.blit(NEW_NUMBER, (j * dif+15, i * dif))
        
    else:
        pygame.draw.rect(SCREEN, WHITE, (j * dif, i * dif, dif , dif ))
    draw_border()
    pygame.display.update()

def cond1(pos):
    x,y=pos[0],pos[1]
    res=False
    if (x>=560 and x<=660 and y>=30 and y<=90):
        res=True
    return res

def cond2(pos):
    x,y=pos[0],pos[1]
    res=False
    if (x>=560 and x<=660 and y>=180 and y<=240):
        res=True
    return res


solve(0,0)

def main():
    pygame.init()
    draw()
    run = True
    while run:
    #     # Loop through the events stored in event.get()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False 
                pygame.quit()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                pos=pygame.mouse.get_pos()
                if (cond1(pos)):
                    Solver(0,0)
                elif (cond2(pos)):
                    Reset()
                else:
                    insert(pos)
            
        # Solver(0,0)
       
        # Solver(0,0)
        


if __name__ =="__main__":
    main()  
