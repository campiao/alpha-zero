import pygame
from pygame.locals import QUIT
import sys
from attaxx.attaxx import Attaxx
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)

RED = (255, 0, 0)
LIGHT_RED = (255, 10, 90)
LIGHTER_RED = (255, 95, 95)
GRAY = (169, 169, 169) 
YELLOW = (249, 166, 3)
LIGHT_YELLOW = (255, 255, 0)
LIGHTER_YELLOW = (241, 235, 156)

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

            pygame.draw.rect(SCREEN, GRAY, (x, y, square_size, square_size), border_radius=5)

            if game[row][col] == 1:
                pygame.draw.circle(SCREEN, BLACK, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)
            elif game[row][col] == -1:
                pygame.draw.circle(SCREEN, WHITE, (x + square_size // 2, y + square_size // 2), square_size // 2 - 10)


def get_font(size): # Returns Press-Start-2P in the desired size
  return pygame.font.Font("images/font.ttf", size) 


def play_attaxx(size):
    offset_x = (1280 - 4 * 100) // 2
    offset_y = (720 - 4 * 100) // 2
    pygame.display.set_caption("Menu")
    game=Attaxx([4,4])
    player=1
    flag=0
    selected_piece = None
    valid_moves = []
    state=game.get_initial_state()
    while True: # Draw the background image
        SCREEN.blit(BG,(0,0))
        Ataxx_MENU_TEXT = get_font(50).render("ATAXX", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(180,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)
        draw_board(state)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                col = (mouse_pos[0] - ((1280 - 400) // 2)) // 100 
                row = (mouse_pos[1] - ((720 - 400) // 2)) // 100 
                if selected_piece is None and state[row][col] == player:
                    # If no piece is selected and the clicked piece belongs to the current player
                    selected_piece = (row, col)
                    valid_moves = game.get_valid_moves(state,player)
                    if flag==0:   # como para fazer um movimento precisamos de ter a posição inicial e a posição para onde queremos ir temos de guardar essas posições
                        flag=1
                        row1=row
                        col1=col
                elif selected_piece:
                    # If a piece is selected and the clicked position is a valid move
                    move = (row1,col1, row, col)
                    action = move[3] + move[2] * 4 + move[1] * 4 ** 2 + move[0] * 4 ** 3
                    game.get_next_state(state,action, player)
                    player = -player  # Switch player after a move
                    selected_piece = None
                    valid_moves = []
                    flag=0
        # if selected_piece:
        #     x, y = selected_piece
        #     x = col * 100 + offset_x
        #     y = row * 100 + offset_y
        #     pygame.draw.rect(SCREEN, LIGHT_YELLOW, (x, y, 100, 100), border_radius=5)
        # # Destacar movimentos válidos
        # for move in valid_moves:
        #     m=game.int_to_move(move)
        #     pygame.draw.rect(SCREEN, YELLOW, ((m[0] - 1) * 100, (m[1] - 1) * 100, 100, 100), border_radius=5)            
        #     print("desenhei")
        pygame.display.update()

if __name__ == "__main__":
    play_attaxx(4)
