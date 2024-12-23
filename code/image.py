import pygame


class Image:
    def __init__(self, file_path: str, width: int, height: int):
        self.file_path = file_path
        self.width = width
        self.height = height
        self.image = pygame.image.load(self.file_path)  # Carrega a imagem a partir do caminho
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Redimensiona a imagem

    def render(self, screen, x, y):
        # Desenha a imagem na tela na posição (x, y)
        screen.blit(self.image, (x, y))
