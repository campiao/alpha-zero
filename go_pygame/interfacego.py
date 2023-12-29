import pygame
from pygame.locals import QUIT
import sys
from go_1 import Go

pygame.init()

# Define as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Define o tamanho do grid e do tabuleiro
GRID_SIZE = SCREEN_WIDTH // 9  # Ajuste conforme necessário
BOARD_SIZE = 7

# Define o modo de exibição
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)

STONE_RADIUS = GRID_SIZE // 2 - 5
BLACK_STONE_COLOR = (0, 0, 0)
WHITE_STONE_COLOR = (255, 255, 255)
BG = pygame.image.load("images/blue_background.jpg")

# Calcular o deslocamento para centralizar o tabuleiro
board_width = min(BOARD_SIZE, SCREEN_WIDTH // GRID_SIZE) * GRID_SIZE
board_height = min(BOARD_SIZE, SCREEN_HEIGHT // GRID_SIZE) * GRID_SIZE
board_x = 330
board_y = 50

def draw_board(go_game):
    board_state = go_game.get_current_state()

    # Desenha o retângulo cinza como fundo
    pygame.draw.rect(SCREEN, GRAY, (board_x, board_y, board_width, board_height))

    for i in range(min(BOARD_SIZE, len(board_state))):
        for j in range(min(BOARD_SIZE, len(board_state[0]))):
            x = board_x + j * GRID_SIZE
            y = board_y + i * GRID_SIZE

            pygame.draw.rect(SCREEN, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)

            stone = board_state[i][j]
            if stone == Go.BLACK:
                pygame.draw.circle(SCREEN, BLACK_STONE_COLOR, (x, y), STONE_RADIUS)
            elif stone == Go.WHITE:
                pygame.draw.circle(SCREEN, WHITE_STONE_COLOR, (x, y), STONE_RADIUS)

    # Draw grid lines
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(SCREEN, BLACK, (board_x + i * GRID_SIZE, board_y),
                         (board_x + i * GRID_SIZE, board_y + board_height), 2)
        pygame.draw.line(SCREEN, BLACK, (board_x, board_y + i * GRID_SIZE),
                         (board_x + board_width, board_y + i * GRID_SIZE), 2)

def play_go(board_size):
    go_game = Go(small_board=True)
    player = 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = (mouse_pos[0] - board_x) // GRID_SIZE
                row = (mouse_pos[1] - board_y) // GRID_SIZE

                if go_game.is_valid_move(go_game.get_current_state(), (row, col), player):
                    go_game.make_move((row, col), player)
                    player = -player  # Switch player after a move

        draw_board(go_game)
        pygame.display.update()

if __name__ == "__main__":
    play_go(7)  # Você pode ajustar o tamanho do tabuleiro conforme necessário
