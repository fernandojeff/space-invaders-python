import datetime
import pygame
import sys

def ranking(screen, background):
    top_jogadores = obter_top_jogadores()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(background, (0, 0))  # Desenha o fundo
        font_title = pygame.font.Font(None, 48)
        font_text = pygame.font.Font(None, 36)
        title = font_title.render("Ranking dos Top 5 Jogadores", True, (255, 255, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 50))
        screen.blit(title, title_rect)
        
        for i, jogador in enumerate(top_jogadores):
            text = font_text.render(f"{i + 1}. {jogador['nome']} - {jogador['pontuacao']} - {jogador['data']}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen.get_width() // 2, 100 + i * 40))
            screen.blit(text, text_rect)
        
        pygame.display.flip()

def gravar_ranking(nome, pontuacao):
    data = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    with open("ranking.txt", "a") as arquivo:
        arquivo.write(f"{nome},{pontuacao},{data}\n")

def perguntar_nome_e_gravar_ranking(pontuacao):
    nome = input("Digite seu nome: ")
    gravar_ranking(nome, pontuacao)
    print("Ranking gravado com sucesso!")

def obter_top_jogadores():
    jogadores = []
    with open("ranking.txt", "r") as arquivo:
        for linha in arquivo:
            nome, pontuacao, data = linha.strip().split(",")
            jogadores.append({"nome": nome, "pontuacao": int(pontuacao), "data": data})
    jogadores.sort(key=lambda x: x["pontuacao"], reverse=True)
    return jogadores[:5]
