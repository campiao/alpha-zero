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

  ataxxSizeBoard = 5
  ataxxPlayer = "human"

  SIZE4X4_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(240, 250), 
                      text_input="4 X 4", font=get_font(30), base_color="#b68f40", hovering_color="White")
  
  SIZE4X4_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(240, 250), 
                      text_input="4 X 4", font=get_font(30), base_color="Green", hovering_color="Green")
  
  SIZE5X5_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250), 
                      text_input="5 X 5", font=get_font(30), base_color="#b68f40", hovering_color="White")
  
  SIZE5X5_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250), 
                      text_input="5 X 5", font=get_font(30), base_color="Green", hovering_color="Green")
  
  SIZE6X6_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(1030, 250), 
                      text_input="6 X 6", font=get_font(30), base_color="#b68f40", hovering_color="White")
  
  SIZE6X6_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(1030, 250), 
                      text_input="6 X 6", font=get_font(30), base_color="Green", hovering_color="Green")
  
  HUMAN_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 450), 
                      text_input="HUMAN", font=get_font(30), base_color="#b68f40", hovering_color="White")

  HUMAN_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 450), 
                      text_input="HUMAN", font=get_font(30), base_color="Green", hovering_color="Green")
  
  ALPHAZERO_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 450), 
                      text_input="ALPHAZERO", font=get_font(30), base_color="#b68f40", hovering_color="White")
  
  ALPHAZERO_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 450), 
                      text_input="ALPHAZERO", font=get_font(30), base_color="Green", hovering_color="Green")
  
  PLAY_BUTTON = Button(image=None, pos=(640, 630), 
                      text_input="PLAY", font=get_font(60), base_color="Green", hovering_color="White")
  
  PLAY_BACK = Button(image=None, pos=(1175,685), 
                      text_input="BACK", font=get_font(20), base_color="White", hovering_color="Red")
  
  buttons=[SIZE4X4_BUTTON, SIZE5X5_BUTTON, SIZE6X6_BUTTON, HUMAN_BUTTON,ALPHAZERO_BUTTON,PLAY_BACK,PLAY_BUTTON]

  while True:
        ATAXX_MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))

        Ataxx_MENU_TEXT = get_font(50).render("ATAXX", True, "#d7fcd4")
        Ataxx_MENU_RECT = Ataxx_MENU_TEXT.get_rect(center=(640,100))
        SCREEN.blit(Ataxx_MENU_TEXT, Ataxx_MENU_RECT)
        
        for button in buttons:
            button.changeColor(ATAXX_MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if SIZE4X4_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                  if SIZE4X4_BUTTON in buttons :
                    buttons.remove(SIZE4X4_BUTTON)
                    buttons.append(SIZE4X4_BUTTON_SELECTED)

                  if SIZE5X5_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE5X5_BUTTON_SELECTED)
                      buttons.append(SIZE4X4_BUTTON_SELECTED)
                      buttons.append(SIZE5X5_BUTTON)

                  if SIZE6X6_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE6X6_BUTTON_SELECTED)
                      buttons.append(SIZE4X4_BUTTON_SELECTED)
                      buttons.append(SIZE6X6_BUTTON)

                  ataxxSizeBoard = 4

                if SIZE5X5_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                  if SIZE5X5_BUTTON in buttons :
                    buttons.remove(SIZE5X5_BUTTON)
                    buttons.append(SIZE5X5_BUTTON_SELECTED)

                  if SIZE4X4_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE4X4_BUTTON_SELECTED)
                      buttons.append(SIZE5X5_BUTTON_SELECTED)
                      buttons.append(SIZE4X4_BUTTON)

                  if SIZE6X6_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE6X6_BUTTON_SELECTED)
                      buttons.append(SIZE5X5_BUTTON_SELECTED)
                      buttons.append(SIZE6X6_BUTTON)

                  goSizeBoard = 5

                if SIZE6X6_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                    if SIZE6X6_BUTTON in buttons :
                      buttons.remove(SIZE6X6_BUTTON)
                      buttons.append(SIZE6X6_BUTTON_SELECTED)

                    if SIZE4X4_BUTTON_SELECTED in buttons:
                        buttons.remove(SIZE4X4_BUTTON_SELECTED)
                        buttons.append(SIZE6X6_BUTTON_SELECTED)
                        buttons.append(SIZE4X4_BUTTON)

                    if SIZE5X5_BUTTON_SELECTED in buttons:
                        buttons.remove(SIZE5X5_BUTTON_SELECTED)
                        buttons.append(SIZE6X6_BUTTON_SELECTED)
                        buttons.append(SIZE5X5_BUTTON)

                    goSizeBoard = 6                  

                if HUMAN_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                  if HUMAN_BUTTON in buttons :
                    buttons.remove(HUMAN_BUTTON)
                    buttons.append(HUMAN_BUTTON_SELECTED)

                  if ALPHAZERO_BUTTON_SELECTED in buttons:
                      buttons.remove(ALPHAZERO_BUTTON_SELECTED)
                      buttons.append(HUMAN_BUTTON_SELECTED)
                      buttons.append(ALPHAZERO_BUTTON)
                  player = "human"

                if ALPHAZERO_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                  if ALPHAZERO_BUTTON in buttons :
                    buttons.remove(ALPHAZERO_BUTTON)
                    buttons.append(ALPHAZERO_BUTTON_SELECTED)

                  if HUMAN_BUTTON_SELECTED in buttons:
                      buttons.remove(HUMAN_BUTTON_SELECTED)
                      buttons.append(ALPHAZERO_BUTTON_SELECTED)
                      buttons.append(HUMAN_BUTTON)

                  player = "alphazero"

                if PLAY_BUTTON.checkForInput(ATAXX_MENU_MOUSE_POS):
                  #jogar(ATAXX,goSizeBoard, player)
                  game_over("ATAXX", "HUMAN", 120, 0)

                if PLAY_BACK.checkForInput(ATAXX_MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def menu_go():
    goSizeBoard = 7
    player = "human"
    
    SIZE7X7_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 250), 
                        text_input="7 X 7", font=get_font(30), base_color="#b68f40", hovering_color="White")
   
    SIZE7X7_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 250), 
                        text_input="7 X 7", font=get_font(30), base_color="Green", hovering_color="Green")
    
    SIZE9X9_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 250), 
                        text_input="9 X 9", font=get_font(30), base_color="#b68f40", hovering_color="White")
    
    SIZE9X9_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 250), 
                        text_input="9 X 9", font=get_font(30), base_color="Green", hovering_color="Green")
    
    HUMAN_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 450), 
                        text_input="HUMAN", font=get_font(30), base_color="#b68f40", hovering_color="White")
    
    HUMAN_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(440, 450), 
                        text_input="HUMAN", font=get_font(30), base_color="Green", hovering_color="Green")
    
    ALPHAZERO_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 450), 
                        text_input="ALPHAZERO", font=get_font(30), base_color="#b68f40", hovering_color="White")
    
    ALPHAZERO_BUTTON_SELECTED = Button(image=pygame.image.load("images/Play Rect.png"), pos=(840, 450), 
                        text_input="ALPHAZERO", font=get_font(30), base_color="Green", hovering_color="Green")
    
    PLAY_BUTTON = Button(image=None, pos=(640, 630), 
                        text_input="PLAY", font=get_font(60), base_color="Green", hovering_color="White")
    
    PLAY_BACK = Button(image=None, pos=(1175,685), 
                        text_input="BACK", font=get_font(20), base_color="White", hovering_color="Red")
                        
    buttons = [HUMAN_BUTTON, ALPHAZERO_BUTTON, SIZE7X7_BUTTON, SIZE9X9_BUTTON,PLAY_BUTTON, PLAY_BACK]
      
    while True:
        GO_MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG,(0,0))

        Go_MENU_TEXT = get_font(50).render("GO", True, "#d7fcd4")
        Go_MENU_RECT = Go_MENU_TEXT.get_rect(center=(640,100))
        SCREEN.blit(Go_MENU_TEXT, Go_MENU_RECT)

        for button in buttons:
            button.changeColor(GO_MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
          if event.type == pygame.MOUSEBUTTONDOWN:
              if SIZE7X7_BUTTON.checkForInput(GO_MENU_MOUSE_POS):
                  if SIZE7X7_BUTTON in buttons :
                    buttons.remove(SIZE7X7_BUTTON)
                    buttons.append(SIZE7X7_BUTTON_SELECTED)

                  if SIZE9X9_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE9X9_BUTTON_SELECTED)
                      buttons.append(SIZE7X7_BUTTON_SELECTED)
                      buttons.append(SIZE9X9_BUTTON)
                  goSizeBoard = 7

              if SIZE9X9_BUTTON.checkForInput(GO_MENU_MOUSE_POS):
                  if SIZE9X9_BUTTON in buttons :
                    buttons.remove(SIZE9X9_BUTTON)
                    buttons.append(SIZE9X9_BUTTON_SELECTED)

                  if SIZE7X7_BUTTON_SELECTED in buttons:
                      buttons.remove(SIZE7X7_BUTTON_SELECTED)
                      buttons.append(SIZE9X9_BUTTON_SELECTED)
                      buttons.append(SIZE7X7_BUTTON)
                  goSizeBoard = 7

              if HUMAN_BUTTON.checkForInput(GO_MENU_MOUSE_POS):
                  if HUMAN_BUTTON in buttons :
                    buttons.remove(HUMAN_BUTTON)
                    buttons.append(HUMAN_BUTTON_SELECTED)

                  if ALPHAZERO_BUTTON_SELECTED in buttons:
                      buttons.remove(ALPHAZERO_BUTTON_SELECTED)
                      buttons.append(HUMAN_BUTTON_SELECTED)
                      buttons.append(ALPHAZERO_BUTTON)
                  player = "human"

              if ALPHAZERO_BUTTON.checkForInput(GO_MENU_MOUSE_POS):
                  if ALPHAZERO_BUTTON in buttons :
                    buttons.remove(ALPHAZERO_BUTTON)
                    buttons.append(ALPHAZERO_BUTTON_SELECTED)

                  if HUMAN_BUTTON_SELECTED in buttons:
                      buttons.remove(HUMAN_BUTTON_SELECTED)
                      buttons.append(ALPHAZERO_BUTTON_SELECTED)
                      buttons.append(HUMAN_BUTTON)
                  player = "alphazero"

              if PLAY_BUTTON.checkForInput(GO_MENU_MOUSE_POS):
                  #jogar(go,goSizeBoard, player)
                  game_over("GO", "HUMAN", 120, 0)
              if PLAY_BACK.checkForInput(GO_MENU_MOUSE_POS):
                  main_menu()

          pygame.display.update()


def game_over(game,winner,pontuacao1, pontuacao2):

  PLAY_BACK = Button(image=None, pos=(1175,685), 
                        text_input="MAIN MENU", font=get_font(20), base_color="Red", hovering_color="White")
  
  buttons = [PLAY_BACK]
  
  while True:

    GAME_OVER_MOUSE_POS = pygame.mouse.get_pos()

    SCREEN.blit(BG,(0,0))

    # GAME_OVER_TEXT = get_font(50).render(game, True, "#d7fcd4")
    # GAME_OVER_RECT = GAME_OVER_TEXT.get_rect(center=(640,100))

    WINNER_TITLE_TEXT = get_font(50).render("WINNER: ", True, "#b68f40")
    WINNER_TITLE_RECT = WINNER_TITLE_TEXT.get_rect(center=(660,150))

    WINNER_TEXT= get_font(80).render(winner, True, "Green")
    WINNER_RECT = WINNER_TEXT.get_rect(center=(640,350))

    PONTUACAO_TEXT = get_font(30).render(f"{pontuacao1} - {pontuacao2}", True, "White")
    PONTUACAO_RECT = PONTUACAO_TEXT.get_rect(center=(640,500))

    # SCREEN.blit(GAME_OVER_TEXT, GAME_OVER_RECT)
    SCREEN.blit(WINNER_TITLE_TEXT, WINNER_TITLE_RECT)
    SCREEN.blit(WINNER_TEXT, WINNER_RECT)
    SCREEN.blit(PONTUACAO_TEXT, PONTUACAO_RECT)

    for button in buttons:
            button.changeColor(GAME_OVER_MOUSE_POS)
            button.update(SCREEN)

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
              if PLAY_BACK.checkForInput(GAME_OVER_MOUSE_POS):
                  main_menu()

            pygame.display.update()


def main_menu():
  pygame.display.set_caption("Menu")

  while True:
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    SCREEN.blit(BG,(0,0))


    ATAXX_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 250), 
                            text_input="ATAXX", font=get_font(50), base_color="#b68f40", hovering_color="White")
    
    GO_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 400), 
                            text_input="GO", font=get_font(50), base_color="#b68f40", hovering_color="White")
    
    QUIT_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#8B0000", hovering_color="White")

    MENU_TEXT = get_font(50).render("SELECIONA O JOGO", True, "#d7fcd4")
    MENU_RECT = MENU_TEXT.get_rect(center=(640,100))

    
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