import pygame
from config import BLACK, GRAY, SCREEN_WIDTH, SCREEN_HEIGHT

def load_and_scale_image(image_path, width, height):
    """Carrega e redimensiona uma imagem."""
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (width, height))

#Desenhar sprites
class SpriteButton:
    def __init__(self, x, y, image, action=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clique com o botão esquerdo
            if self.rect.collidepoint(event.pos):  # Verifica se o clique foi no botão
                if self.action:
                    self.action()

# Função para desenhar um botão sem ser sprites
def draw_button(screen, text, x, y, width, height, active_color, inactive_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = active_color if x < mouse[0] < x + width and y < mouse[1] < y + height else inactive_color
    pygame.draw.rect(screen, color, (x, y, width, height))

    # Renderizar texto
    from config import FONT
    text_surface = FONT.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

    # Verificar clique
    if click[0] == 1 and action:
        pygame.time.delay(200)  # Evitar múltiplos cliques rápidos
        action()

def gerenciar_monstros(screen, linhas, colunas, sprite, velocidade, delta_time, y_nave):
    # Carregar sprite do monstro e redimensionar
    img_monstro_original = pygame.image.load(sprite)
    largura_desejada = 25  # Tamanho do monstro
    altura_desejada = 25   
    img_monstro = pygame.transform.scale(img_monstro_original, (largura_desejada, altura_desejada))
    
    largura_monstro = img_monstro.get_width()
    altura_monstro = img_monstro.get_height()

    # Espaçamento entre monstros
    espacamento_x = largura_monstro // 2
    espacamento_y = altura_monstro // 2

    # Margem inicial
    margem_inicial = 10

    # Inicializar matriz de monstros 
    if not hasattr(gerenciar_monstros, "monstros"):
        gerenciar_monstros.monstros = [
            [
                {
                    "x": margem_inicial + j * (largura_monstro + espacamento_x), 
                    "y": margem_inicial + i * (altura_monstro + espacamento_y)  
                }
                for j in range(colunas)
            ]
            for i in range(linhas)
        ]
        gerenciar_monstros.direcao = 1 

    # Verificar se a lista de monstros está vazia
    if not any(gerenciar_monstros.monstros):
        return False  # Todos os monstros foram eliminados

    # Verificar se algum monstro atingiu a parede
    limite_esquerdo = min(monstro["x"] for linha in gerenciar_monstros.monstros for monstro in linha)
    limite_direito = max(monstro["x"] + largura_monstro for linha in gerenciar_monstros.monstros for monstro in linha)

    # Inverter direção e descer monstros se necessário
    if limite_esquerdo <= 0 or limite_direito >= SCREEN_WIDTH:
        gerenciar_monstros.direcao *= -1  # Inverter direção de movimento
        for linha in gerenciar_monstros.monstros:
            for monstro in linha:
                monstro["y"] += altura_monstro // 0.8  # Todos os monstros descem um pouco

    # Atualizar posição dos monstros
    for linha in gerenciar_monstros.monstros:
        for monstro in linha:
            monstro["x"] += gerenciar_monstros.direcao * velocidade * delta_time

    # Desenhar monstros na tela
    for linha in gerenciar_monstros.monstros:
        for monstro in linha:
            screen.blit(img_monstro, (monstro["x"], monstro["y"]))

    # Verificar fim de jogo
    monstro_mais_baixo = max(monstro["y"] + altura_monstro for linha in gerenciar_monstros.monstros for monstro in linha)
    if monstro_mais_baixo >= y_nave:
        return True  # Game over

    return False  # Jogo continua

def reiniciar_monstros(colunas, linhas):

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

# Função para desenhar tiros dos monstros
def desenha_tiro_monstro(screen, x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 5, 15))  # Retângulo vermelho

def desenha_nave(screen, img_nave, x, y):
    screen.blit(img_nave, (x, y))

def desenha_tiro(screen, sprites_tiro, x, y, frame):
    screen.blit(sprites_tiro[frame], (x, y))

def desenha_vidas(screen, vidas):
    # Exibir vidas
    font = pygame.font.SysFont(None, 30)
    vidas_text = font.render(f"Vidas: {vidas}", True, (255, 255, 255))
    screen.blit(vidas_text, (10, 10))

#Desenha o FPS na tela
def desenha_fps(screen, clock):
    font = pygame.font.SysFont(None, 30) #Define fonte e tamanho dela
    fps = clock.get_fps()
    fps_text = font.render(f"{fps:.0f}", True, (255, 255, 255))
    screen.blit(fps_text, (775, 575))

# Função para desenhar a pontuação na tela
def desenhar_pontuacao(screen, pontuacao):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Pontuação: {pontuacao}", True, (255, 255, 255))
    screen.blit(text, (620, 10))

