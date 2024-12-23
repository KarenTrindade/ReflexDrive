import pygame
from code.gameManager import GameManager
from code.menu import Menu
from config import WIDTH, HEIGHT

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Reflex Drive")

# Criação do menu
menu = Menu(screen)

# Criação do GameManager com o menu
game_manager = GameManager(screen, menu)

# Loop principal do jogo
running = True
while running:
    # Processamento de eventos e atualização do estado do jogo
    game_manager.handle_events()
    game_manager.update()

    # Atualização da tela
    pygame.display.flip()

# Encerramento do Pygame
pygame.quit()
