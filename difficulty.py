import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, button_width, button_height
from utils import SpriteButton, load_and_scale_image

def dificuldade(screen, main_menu):
    # Carrega a imagem de fundo
    background = pygame.image.load("images/background.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensiona se necessário

     # Carregar e redimensionar as imagens dos botões
    btn_facil_img = load_and_scale_image("images/dificuldades/facil.png", button_width, button_height)
    btn_medio_img = load_and_scale_image("images/dificuldades/medio.png", button_width, button_height)
    btn_dificil_img = load_and_scale_image("images/dificuldades/dificil.png", button_width, button_height)
    btn_voltar_img = load_and_scale_image("images/voltar.png", button_width, button_height)

    # Criar os botões com as imagens redimensionadas
    btn_facil = SpriteButton(300, 200, btn_facil_img, lambda: print("Nível Fácil selecionado"))
    btn_medio = SpriteButton(300, 300, btn_medio_img, lambda: print("Nível Médio selecionado"))
    btn_dificil = SpriteButton(300, 400, btn_dificil_img, lambda: print("Nível Difícil selecionado"))
    btn_voltar = SpriteButton(300, 500, btn_voltar_img, lambda: main_menu(screen))
    buttons = [btn_facil, btn_medio, btn_dificil, btn_voltar]

    running = True
    while running:
        # Desenha a imagem de fundo
        screen.blit(background, (0, 0))

        # Desenha os botões
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
