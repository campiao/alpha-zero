import pygame
from pygame.locals import QUIT
import sys
import time
import torch
from torch.optim import Adam
import numpy as np
from go_pygame.go_1 import Go
from alphazero import ResNet
from alphazero import MCTS

import os
pygame.init()

# Define as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Define o tamanho do grid e do tabuleiro
GRID_SIZE = 75  # Ajuste conforme necessário


# Define o modo de exibição
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("GO")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

STONE_RADIUS = GRID_SIZE // 2 - 5
BLACK_STONE_COLOR = (0, 0, 0)
WHITE_STONE_COLOR = (255, 255, 255)
BG = pygame.image.load("images/blue_background.jpg")



def get_font(size): # Returns Press-Start-2P in the desired size
  return pygame.font.Font("images/font.ttf", size) 


def draw_board(board_state):
    board_size = len(board_state)

    offset_x = (1280 - board_size * GRID_SIZE) // 2 
    offset_y = (720 - board_size * GRID_SIZE) // 2 
    # Desenha o retângulo cinza como fundo

    for i in range(board_size-1):
        for j in range(board_size-1):
            x = j * GRID_SIZE + offset_x +50
            y = i * GRID_SIZE + offset_y +50
            pygame.draw.rect(SCREEN, GRAY, (x, y, GRID_SIZE, GRID_SIZE), border_radius=15)
    for i in range(board_size):
        for j in range(board_size):
            x = j * GRID_SIZE + offset_x +50
            y = i * GRID_SIZE + offset_y +50
            stone = board_state[i][j]
            if stone == Go.BLACK:
                pygame.draw.circle(SCREEN, BLACK_STONE_COLOR, (x, y), STONE_RADIUS)
            elif stone == Go.WHITE:
                pygame.draw.circle(SCREEN, WHITE_STONE_COLOR, (x, y), STONE_RADIUS)


def prepair_model(game):
    args = {
            'game': 'Go',
            'num_iterations': 10,             # number of highest level iterations
            'num_selfPlay_iterations': 10,   # number of self-play games to play within each iteration
            'num_mcts_searches': 100,         # number of mcts simulations when selecting a move within self-play
            'num_epochs': 25,                  # number of epochs for training on self-play data for each iteration
            'batch_size': 8,                # batch size for training
            'temperature': 1.25,              # temperature for the softmax selection of moves
            'C': 2,                           # the value of the constant policy
            'augment': False,                 # whether to augment the training data with flipped states
            'dirichlet_alpha': 0.3,           # the value of the dirichlet noise
            'dirichlet_epsilon': 0.25,        # the value of the dirichlet noise
            'alias': ('Go1234')
    }
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = ResNet(game, 9, 3, device)
    model.load_state_dict(torch.load(f'AlphaZero/Models/Go1234/model_2.pt', map_location=device))
    #optimizer.load_state_dict(torch.load(f'AlphaZero/Models/Attax_TestModel/optimizer_4.pt', map_location=device))
    mcts = MCTS(model, game, args)
    return mcts


def play_go(board_size):
    go_game = Go(board_size)
    player = 1
    action=0
    state=go_game.get_initial_state()
    mcts=prepair_model(go_game)
    if board_size == 7: margin = 1 
    else: margin = 2
    while True:
        SCREEN.blit(BG,(0,0))
        Ataxx_MENU_TEXT = get_font(50).render("GO", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(180,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)
        draw_board(state)
        print(state)
        if player==1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    col = (mouse_pos[0] - ((1280 - 400) // 2)) // 75 +margin
                    row = (mouse_pos[1] - ((720 - 400) // 2)) // 75 +margin

                    print(col, row)
                    if  row >=0 and col >=0  and row < board_size and col < board_size:
                        action=col + row * board_size
                        if   go_game.is_valid_move(state, action, player):
                            state=go_game.get_next_state(state,action, player)
                            player = -player  # Switch player after a move
                            draw_board(state)
                            print(state)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        player = -player
        else:
            time.sleep(1)
            neut = go_game.change_perspective(state, -player)
            action = mcts.search(neut, player)
            action = np.argmax(action)
            state = go_game.get_next_state(state, action, player)
            player = -player
        winner, win = go_game.get_value_and_terminated(state, action,player)
        if win:
            return go_game.count_influenced_territory_enhanced(state)
        pygame.display.update()

if __name__ == "__main__":
    play_go(7)  # Você pode ajustar o tamanho do tabuleiro conforme necessário
