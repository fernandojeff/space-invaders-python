import pygame
import sys
from game import jogar
from difficulty import dificuldade
from ranking import ranking
from config import SCREEN_WIDTH, SCREEN_HEIGHT, button_width, button_height
from utils import SpriteButton, load_and_scale_image

def main_menu(screen):
    #Cria imagem do fundo
    background = pygame.image.load("images/background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  

    #Desenha a imagem de cima
    def draw_header():
        header_image = pygame.image.load("images/header.png").convert_alpha()

        header_image = pygame.transform.scale(header_image, (513, 151))

        screen.blit(header_image, (158, 10))

    # Carregar e redimensionar imagens dos botões
    jogar_img = load_and_scale_image("images/jogar.png", button_width, button_height)
    dificuldade_img = load_and_scale_image("images/dificuldade.png", button_width, button_height)
    ranking_img = load_and_scale_image("images/ranking.png", button_width, button_height)
    sair_img = load_and_scale_image("images/sair.png", button_width, button_height)

    # Criar botões
    btn_jogar = SpriteButton(300, 200, jogar_img, lambda: jogar(screen))
    btn_dificuldade = SpriteButton(300, 300, dificuldade_img, lambda: dificuldade(screen, main_menu))
    btn_ranking = SpriteButton(300, 400, ranking_img, lambda: ranking(screen, background))
    btn_sair = SpriteButton(300, 500, sair_img, lambda: pygame.quit() or sys.exit())
    buttons = [btn_jogar, btn_dificuldade, btn_ranking, btn_sair]

    running = True
    while running:
        screen.blit(background, (0, 0))  
        
        draw_header()

        for button in buttons:
            button.draw(screen)
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  
                sys.exit()

            # Lida com eventos de clique para cada botão
            for button in buttons:
                button.handle_event(event)

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Space Invaders by Fernando")
    main_menu(screen)
