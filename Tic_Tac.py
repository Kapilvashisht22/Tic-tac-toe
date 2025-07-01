import pygame 
import numpy as np
import sys

# Initialise pygame
pygame.init()

# constants
WIDTH , HEIGHT =300,300
LINE_WIDTH=5
ROWS,COLS=3,3
SQUARE_SIZE = WIDTH // COLS

# define color
BG_COLOR =(255,255,255)
LINE_COLOR=(0,0,0)
X_COLOR=(255,0,0)
O_COLOR=(0,0,255)

# Set up the screen
screen =pygame.display.set_mode((WIDTH ,HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Game state variable board
board =[["" for _ in range(COLS)]for  _ in range(ROWS)]
player="X"
game_over =False

def draw_board():
    screen.fill(BG_COLOR)
    # Draw grid lines
    for i in range(1,ROWS):

        #  pygame.draw.line(surface, color, start_pos, end_pos, width)

        pygame.draw.line(screen , LINE_COLOR, (0,i*SQUARE_SIZE),(WIDTH,i*SQUARE_SIZE),LINE_WIDTH)
        pygame.draw.line(screen , LINE_COLOR,(i * SQUARE_SIZE,0),(i * SQUARE_SIZE, HEIGHT),LINE_WIDTH) 
    # draw  Xs and Os
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col]=="X":    
                #Draw x
                 
                start1=(col*SQUARE_SIZE + 20,row* SQUARE_SIZE + 20)  # Here 20 represent padding
                end1 =(col*SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + SQUARE_SIZE -20)
                start2=(col*SQUARE_SIZE+ 20,row * SQUARE_SIZE +SQUARE_SIZE - 20)
                end2=(col*SQUARE_SIZE + SQUARE_SIZE - 20, row * SQUARE_SIZE + 20)
                pygame.draw.line(screen, X_COLOR, start1, end1,LINE_WIDTH)
                pygame.draw.line(screen, X_COLOR, start2, end2,LINE_WIDTH) 
            elif board[row][col]=="O":
                #Draw O
                center =(col * SQUARE_SIZE +SQUARE_SIZE // 2 , row * SQUARE_SIZE +SQUARE_SIZE //2)
                pygame.draw.circle(screen , O_COLOR , center ,SQUARE_SIZE //3 ,LINE_WIDTH)
def check_winner(player): 
        # rows and columns       
    for i in range(ROWS):
        if all (board[i][j]==player for j in range( COLS)) or all(board[j][i]== player for j in range(ROWS)):
            return True
            # Diagonals
    if all (board[i][i]==player for i in range( ROWS)) or all(board[i][ROWS -1-i]== player for i in range(ROWS)):
        return True 
    return False
def check_draw():
    for row in board:
        for cell in row:
            if cell =="":
                return False
    return True
    # Main loop
while True:
    draw_board()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type== pygame.MOUSEBUTTONDOWN and not game_over:
            x,y =event.pos
            row=y// SQUARE_SIZE 
            col =x//SQUARE_SIZE
            if board [row][col]=="":
                board[row][col]= player
                if check_winner(player):
                    print(f"Player {player} wins!")
                    game_over =True
                elif check_draw():
                    print("It's a draw!")
                    game_over = True
                else :
                    player ="O" if player =="X" else "X"
    # draw_board()
    pygame.display.update()
                    