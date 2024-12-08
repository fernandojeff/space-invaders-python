import pygame
import sys
from config import WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, dificuldade
from utils import gerenciar_monstros

def jogar(screen):
    debug = True #True para ativar o FPS
    
    # Carregar imagem da nave
    img_nave = pygame.image.load('images/nave.png')
    largura_nave = img_nave.get_width()
    altura_nave = img_nave.get_height()

    # Configurações da matriz de monstros
    linhas = 5
    colunas = 10
    sprite_monstro = 'images/monstro.png'
    velocidade_monstros = 60 * dificuldade

    # Carregar sprites do tiro
    sprites_tiro = [
        pygame.image.load(f'images/tiro/tiro_{i}.png') for i in range(1, 4)
    ]
    largura_tiro = sprites_tiro[0].get_width()
    altura_tiro = sprites_tiro[0].get_height()

    # Posição inicial da nave
    x_nave = SCREEN_WIDTH // 2 - largura_nave // 2
    y_nave = SCREEN_HEIGHT - altura_nave - 10

    # Velocidade de movimento da nave
    velocidade_nave = 400 * dificuldade

    # Velocidade do tiro
    velocidade_tiro = 1000

    # Lista de tiros ativos
    tiros = []

    # Tempo de recarga do tiro
    tempo_recarga = 0.5 / dificuldade
    ultimo_tiro = 0

    # Frame do sprite do tiro
    frame_tiro = 0
    tempo_sprite_tiro = 0.1  # Tempo entre frames (em segundos)
    ultimo_frame = 0

    def desenha_nave(x, y):
        screen.blit(img_nave, (x, y))

    def desenha_tiro(x, y, frame):
        screen.blit(sprites_tiro[frame], (x, y))
    
    #Desenha o FPS na tela
    def desenha_fps():
        font = pygame.font.SysFont(None, 30) #Define fonte e tamanho dela
        fps = clock.get_fps()
        fps_text = font.render(f"{fps:.0f}", True, (255, 255, 255))
        screen.blit(fps_text, (775, 575))
        
    # Clock para controlar o FPS
    clock = pygame.time.Clock()

    def verificar_colisao(tiro, monstro):
        return (
            tiro[0] < monstro["x"] + 25 and
            tiro[0] + largura_tiro > monstro["x"] and
            tiro[1] < monstro["y"] + 25 and
            tiro[1] + altura_tiro > monstro["y"]
        )

    def reiniciar_monstros():
        gerenciar_monstros.monstros = [
            [
                {
                    "x": 10 + j * (25 + 12),  # 25 é a largura do monstro, 12 é o espaçamento
                    "y": 10 + i * (25 + 12)   # 25 é a altura do monstro, 12 é o espaçamento
                }
                for j in range(colunas)
            ]
            for i in range(linhas)
        ]
        gerenciar_monstros.direcao = 1

    # Inicializar monstros
    reiniciar_monstros()

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        delta_time = clock.tick(60) / 1000  # Tempo decorrido no frame atual

        # Atualizar a tela de fundo
        screen.fill((0, 0, 0))

        # Obter as teclas pressionadas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            x_nave -= velocidade_nave * delta_time
        if teclas[pygame.K_RIGHT]:
            x_nave += velocidade_nave * delta_time

        # Limitar o movimento da nave aos limites da tela
        if x_nave < 0:
            x_nave = 0
        elif x_nave > SCREEN_WIDTH - largura_nave:
            x_nave = SCREEN_WIDTH - largura_nave

        # Controle do tiro
        tempo_atual = pygame.time.get_ticks() / 1000  # Tempo em segundos
        if teclas[pygame.K_SPACE] and tempo_atual - ultimo_tiro > tempo_recarga:
            # Adicionar um novo tiro à lista
            tiros.append([x_nave + largura_nave // 2 - largura_tiro // 2, y_nave])
            ultimo_tiro = tempo_atual

        # Atualizar frame do sprite do tiro
        if tempo_atual - ultimo_frame > tempo_sprite_tiro:
            frame_tiro = (frame_tiro + 1) % len(sprites_tiro)  # Ciclo entre 0, 1, 2
            ultimo_frame = tempo_atual

        for tiro in tiros[:]:
            tiro[1] -= velocidade_tiro * delta_time  
            if tiro[1] < -altura_tiro:  
                tiros.remove(tiro)

        # Verificar colisões
        tiros_para_remover = []
        monstros_para_remover = []
        for tiro in tiros:
            for linha in gerenciar_monstros.monstros:
                for monstro in linha:
                    if verificar_colisao(tiro, monstro):
                        tiros_para_remover.append(tiro)
                        monstros_para_remover.append(monstro)
                        break

        for tiro in tiros_para_remover:
            if tiro in tiros:
                tiros.remove(tiro)

        for monstro in monstros_para_remover:
            for linha in gerenciar_monstros.monstros:
                if monstro in linha:
                    linha.remove(monstro)

        # Desenhar a nave e os tiros
        desenha_nave(x_nave, y_nave)
        for tiro in tiros:
            desenha_tiro(tiro[0], tiro[1], frame_tiro)

        if debug:
            desenha_fps()

        # Gerenciar monstros
        if gerenciar_monstros(screen, linhas, colunas, sprite_monstro, velocidade_monstros, delta_time, y_nave):
            print("Game Over!")
            running = False

        # Verificar se todos os monstros foram eliminados
        if not any(gerenciar_monstros.monstros):
            print("Você venceu!")
            reiniciar_monstros()
            running = False

        # Atualizar o display
        pygame.display.update()

        # Limitar o FPS a 60
        clock.tick(60)
