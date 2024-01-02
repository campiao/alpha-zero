import pygame
from pygame.locals import QUIT
import sys
import numpy as np
from attaxx.attaxx import Attaxx
pygame.init()
from alphazero import MCTS
import torch
from alphazero import ResNet
import time

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 250)
GRAY = (169, 169, 169) 

# Load the background image
BG = pygame.image.load("images/blue_background.jpg")


def draw_board(game):
    board_size = len(game)
    square_size = 100

    offset_x = (1280 - board_size * square_size) // 2
    offset_y = (720 - board_size * square_size) // 2

    for row in range(board_size):
        for col in range(board_size):
            x = col * square_size + offset_x
            y = row * square_size + offset_y

            pygame.draw.rect(SCREEN, GRAY, (x, y, square_size, square_size), border_radius=15)

            if game[row][col] == 1:
                pygame.draw.circle(SCREEN, BLACK, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)
            elif game[row][col] == -1:
                pygame.draw.circle(SCREEN, WHITE, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)


def get_font(size): # Returns Press-Start-2P in the desired size
  return pygame.font.Font("images/font.ttf", size) 



def prepair_model(game):
    args = {
            'game': 'Attaxx',
            'num_iterations': 8,              # number of highest level iterations
            'num_selfPlay_iterations': 400,   # number of self-play games to play within each iteration
            'num_mcts_searches': 60,          # number of mcts simulations when selecting a move within self-play
            'num_epochs': 4,                  # number of epochs for training on self-play data for each iteration
            'batch_size': 40,                 # batch size for training
            'temperature': 1.25,              # temperature for the softmax selection of moves
            'C': 2,                           # the value of the constant policy
            'augment': False,                 # whether to augment the training data with flipped states
            'dirichlet_alpha': 0.3,           # the value of the dirichlet noise
            'dirichlet_epsilon': 0.125,       # the value of the dirichlet noise
            'alias': ('Attaxx_final12_6')
        }
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(game, 9, 64, device)
    model.load_state_dict(torch.load(f'AlphaZero/Models/Attaxx_final2_4/model_99.pt', map_location=device))
    #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
    mcts = MCTS(model, game, args)
    return mcts



def play_attaxx(size):
    offset_x = (1280 - size * 100) // 2
    offset_y = (720 - size * 100) // 2
    pygame.display.set_caption("Menu")
    game=Attaxx([size,size])
    mcts=prepair_model(game)
    square_size=100
    row1=0
    col1=0
    count1 =0
    count2=0 
    flag=0
    player=1
    selected_piece = None
    valid_moves = []
    state=game.get_initial_state()
    while True: # Draw the background image
        SCREEN.blit(BG,(0,0))
        Ataxx_MENU_TEXT = get_font(50).render("ATAXX", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(180,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)
        Ataxx_Pontuacao_TEXT = get_font(30).render(f"HUMAN {count1} - {count2} ALPHAZERO", True, "#d7fcd4")
        Ataxx_Pontuacao_Rect = Ataxx_Pontuacao_TEXT.get_rect(center=(700,650))
        SCREEN.blit(Ataxx_Pontuacao_TEXT,Ataxx_Pontuacao_Rect)
        draw_board(state)
        if player==1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = (mouse_pos[0] - offset_x) // 100
                    row = (mouse_pos[1] - offset_y) // 100 
                    if selected_piece is None and state[row][col] == player:
                        print("selecionei")
                        # If no piece is selected and the clicked piece belongs to the current player
                        selected_piece = (row, col)
                        valid_moves = game.get_moves_at_point(state,player,row,col)
                        if flag==0:   
                            flag=1
                            row1=row
                            col1=col
                    elif selected_piece:
                        if row1==row and col1==col:
                            print("same piece")
                            selected_piece = None
                            valid_moves = []
                            flag=0
                        elif (row1,col1,row, col) in valid_moves:
                            print("movendo")
                            move = (row1,col1, row, col)
                            action = move[3] + move[2] * size + move[1] * size ** 2 + move[0] * size ** 3
                            state=game.get_next_state(state,action, player)
                            selected_piece = None
                            valid_moves = []
                            flag=0
                            draw_board(state)
                            player = -player
                    print(state)
            if selected_piece:
                x = col * square_size + offset_x
                y = row * square_size + offset_y
                pygame.draw.circle(SCREEN, LIGHT_BLUE, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)
            # Destacar movimentos válidos
                for move in valid_moves:
                    x = move[3] * square_size + offset_x
                    y = move[2] * square_size + offset_y
                    pygame.draw.circle(SCREEN, LIGHT_BLUE, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)        
        elif player==-1:
            print("maquina")
            time.sleep(1)
            neut = game.change_perspective(state, -player)
            action = mcts.search(neut, player)
            action = np.argmax(action)
            state = game.get_next_state(state, action, player)
            player=-player  # Switch player after a move
        winner, win,count1,count2 = game.check_win_and_over(state, action=None)
        if win:
            return winner,count1,count2
        pygame.display.update()

if __name__ == "__main__":
    play_attaxx(4)
