import pygame
from pygame.locals import QUIT
import sys
from go_1 import Go

pygame.init()

# Define as dimensões da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800

# Define o tamanho do grid e do tabuleiro
GRID_SIZE = 75  # Ajuste conforme necessário
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



def get_font(size): # Returns Press-Start-2P in the desired size
  return pygame.font.Font("images/font.ttf", size) 


def draw_board(go_game):
    board_state = go_game.get_current_state()
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


def play_go(board_size):
    go_game = Go(small_board=True)
    player = 1

    while True:
        SCREEN.blit(BG,(0,0))
        Ataxx_MENU_TEXT = get_font(50).render("GO", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(180,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = (mouse_pos[0] - ((1280 - 400) // 2)) // 100 +1
                row = (mouse_pos[1] - ((720 - 400) // 2)) // 100 +1

                print(col, row)
                print(go_game.get_current_state())
                if go_game.is_valid_move(go_game.get_current_state(), (row, col), player) and go_game.get_current_state()[row][col] == 0 and row >=0 and col >=0 :
                    print("move")
                    go_game.make_move((row, col), player)
                    player = -player  # Switch player after a move
        x, y, player = hover_to_select(player, valid_moves, click)
        draw_board(go_game)
        pygame.display.update()

if __name__ == "__main__":
    play_go(9)  # Você pode ajustar o tamanho do tabuleiro conforme necessário
