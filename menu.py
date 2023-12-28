import pygame,sys
from button import Button 
#from ataxx import ataxx

pygame.init()

SCREEN = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Menu")


BG = pygame.image.load("images/blue_background.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
  return pygame.font.Font("images/font.ttf", size)

def menu_ataxx():
  while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))

        Ataxx_MENU_TEXT = get_font(50).render("ATAXX", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(640,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)

        SIZE4X4_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(240, 250), 
                            text_input="4 X 4", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        SIZE5X5_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="5 X 5", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        SIZE6X6_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1030, 250), 
                            text_input="6 X 6", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        HUMAN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 450), 
                            text_input="HUMAN", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        ALPHAZERO_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(840, 450), 
                            text_input="ALPHAZERO", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        
        HUMAN_BUTTON.changeColor(PLAY_MOUSE_POS)
        HUMAN_BUTTON.update(SCREEN)
        ALPHAZERO_BUTTON.changeColor(PLAY_MOUSE_POS)
        ALPHAZERO_BUTTON.update(SCREEN)
        SIZE4X4_BUTTON.changeColor(PLAY_MOUSE_POS)
        SIZE4X4_BUTTON.update(SCREEN)
        SIZE5X5_BUTTON.changeColor(PLAY_MOUSE_POS)
        SIZE5X5_BUTTON.update(SCREEN)
        SIZE6X6_BUTTON.changeColor(PLAY_MOUSE_POS)
        SIZE6X6_BUTTON.update(SCREEN)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def menu_go():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Go_MENU_TEXT = get_font(50).render("GO", True, "#d7fcd4")
        Go_MENU_RECT = Go_MENU_TEXT.get_rect(center=(640,100))
        SCREEN.blit(Go_MENU_TEXT, Go_MENU_RECT)

        SIZE7X7_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="7 X 7", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        SIZE9X9_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(840, 250), 
                            text_input="9 X 9", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        
        HUMAN_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 450), 
                            text_input="HUMAN", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        ALPHAZERO_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(840, 450), 
                            text_input="ALPHAZERO", font=get_font(30), base_color="#b68f40", hovering_color="White")
        
        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(30), base_color="White", hovering_color="Green")
        
        HUMAN_BUTTON.changeColor(PLAY_MOUSE_POS)
        HUMAN_BUTTON.update(SCREEN)
        ALPHAZERO_BUTTON.changeColor(PLAY_MOUSE_POS)
        ALPHAZERO_BUTTON.update(SCREEN)
        SIZE7X7_BUTTON.changeColor(PLAY_MOUSE_POS)
        SIZE7X7_BUTTON.update(SCREEN)
        SIZE9X9_BUTTON.changeColor(PLAY_MOUSE_POS)
        SIZE9X9_BUTTON.update(SCREEN)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for button in [HUMAN_BUTTON, ALPHAZERO_BUTTON, SIZE7X7_BUTTON, SIZE9X9_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SIZE7X7_BUTTON.checkForInput(MENU_MOUSE_POS):
                    SIZE7X7_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="7 X 7", font=get_font(30), base_color="#8B0000", hovering_color="White")
                if SIZE9X9_BUTTON.checkForInput(MENU_MOUSE_POS):
                    SIZE9X9_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(440, 250), 
                            text_input="9 X 9", font=get_font(30), base_color="#FFFFFF", hovering_color="White")
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
  pygame.display.set_caption("Menu")

  while True:
    SCREEN.blit(BG,(0,0))

    MENU_MOUSE_POS = pygame.mouse.get_pos()

    ATAXX_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="ATAXX", font=get_font(50), base_color="#b68f40", hovering_color="White")
    
    GO_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="GO", font=get_font(50), base_color="#b68f40", hovering_color="White")
    
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#8B0000", hovering_color="White")

    MENU_TEXT = get_font(50).render("SELECIONA O JOGO", True, "#d7fcd4")
    MENU_RECT = MENU_TEXT.get_rect(center=(640,100))

    #ATAXX_BUTTON = Button()

    SCREEN.blit(MENU_TEXT,MENU_RECT)

    for button in [ATAXX_BUTTON, GO_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ATAXX_BUTTON.checkForInput(MENU_MOUSE_POS):
                menu_ataxx()
            if GO_BUTTON.checkForInput(MENU_MOUSE_POS):
                menu_go()
            if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

    pygame.display.update()

main_menu()