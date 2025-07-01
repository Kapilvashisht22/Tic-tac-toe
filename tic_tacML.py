import pygame
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Step :1 Generate training Data

def generate_smart_game():
    board=[0]*9 
    game_data=[]
    for turn in range(9):
        player = 1 if turn %2==0 else -1
        available=[i for i in range(9) if board[i]==0]
        if not available:
            break
        move= random.choice(available)
        current_board = board.copy() 
        board[move]=player
        game_data.append((current_board,move))
        if check_winner(board,player):
            break
    return game_data
def check_winner (board,player):
    win_positions =[
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8], 
        [0,4,8],[2,4,6]
    ]
    for pos in win_positions:
        if all(board[i]==player for i in pos):
            return True
    return False
# Generate training data
X,y=[],[]   
for _ in range(10000):      # we donot need the value of variable so we place _
    game =generate_smart_game()
    for state,move in game:
        if state[move]==0:   # only valid move
            X.append(state)
            y.append(move)
X =np.array(X)
y =np.array(y)

# Train the ML model
model= DecisionTreeClassifier(max_depth=10,min_samples_split=10)
X_train,X_test,y_train,y_test = train_test_split( X , y ,test_size=0.2)
model.fit(X_train,y_train)
print(f'Model trained.Accuracy:{accuracy_score ( y_test ,model.predict(X_test)):.2f}')
# step:5 pygame setup


# Initialise pygame
pygame.init()

# constants
WIDTH , HEIGHT =300,300
LINE_WIDTH=5
CELL_SIZE=WIDTH//3


# define color
WHITE =(255,255,255)
LINE_COLOR=(0,0,0)
X_COLOR=(200,0,0)
O_COLOR=(0,0,200)
Font =pygame.font.SysFont(None ,60)
# Set up the screen
screen =pygame.display.set_mode((WIDTH ,HEIGHT))
pygame.display.set_caption("Tic Tac Toe with ML")

board=[0]*9  # initial empty board
def draw_board():
    screen.fill(WHITE)
    for  i in range(1,3):
        pygame.draw.line(screen , LINE_COLOR, (0,i*CELL_SIZE),(WIDTH,i*CELL_SIZE),LINE_WIDTH)
        pygame.draw.line(screen , LINE_COLOR,(i * CELL_SIZE,0),(i * CELL_SIZE, HEIGHT),LINE_WIDTH) 
    for i in range(9):
        X =(i%3) *CELL_SIZE
        y=(i//3)* CELL_SIZE
        if board[i]==1:
            text =Font.render('X',True,X_COLOR)
            screen.blit(text,(X+30,y+20))
        elif board[i]== -1:
            text =Font.render('O',True,O_COLOR)
            screen.blit(text,(X+30,y+20))
    pygame.display.update()
def game_over(message):
    print(message)
    pygame.time.display(1500)
    global board,player_turn
    board=[0]*9
    player_turn=True

running=True
player_turn=True

while running:
    draw_board()
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN and player_turn:  # enumerate join value and board
            mouseX ,mouseY= event.pos
            row= mouseY // CELL_SIZE
            col= mouseX // CELL_SIZE
            idx = row*3 +col
            if board[idx]==0:
                board[idx]=1
                if check_winner(board,1):
                    game_over("You Win!")
                    continue
                elif all(cell !=0 for cell in board):
                    game_over("Draw!")
                    continue
                player_turn =False
    if not player_turn and any(cell==0 for cell in board):
        input_board =np.array(board).reshape(1,-1)
        pred_move = model.predict(input_board)[0]
        while board[pred_move] !=0:
            pred_move= random.choice([i for i, val in enumerate(board) if val==0])
        board[pred_move]=-1
        if check_winner(board,-1):
            game_over("Computer Wins!")
        elif all(cell !=0 for cell in board):
            game_over("Draw!")
        else:
            player_turn =True


pygame.quit()