import pygame


class Player:
    def __init__(self, x, y, speed, screen_width, screen_height):

        # Inicializa o jogador com uma posição inicial, velocidade e redimensionamento da imagem.

        self.x = x
        self.y = y
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Imagem do jogador
        self.image = pygame.image.load("assets/images/carros/Car_1_01.png")
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.07), int(screen_height * 0.2)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Largura da estrada (60% da largura da tela)
        self.road_width = int(screen_width * 0.6)

        # Limite esquerdo da estrada
        self.road_left = (screen_width - self.road_width) // 2 + int(self.road_width * 0.05)

        self.road_right = self.road_left + self.road_width - self.rect.width + 20  # Aumenta 20px no limite direito

        # Ajustando a posição inicial do carro para garantir que ele comece dentro da estrada
        # Ajuste da posição horizontal (esquerda/direita)
        self.rect.x = max(self.rect.x,
                          self.road_left)  # Garante que o carro comece dentro do limite esquerdo da estrada
        self.rect.x = min(self.rect.x,
                          self.road_right - self.rect.width)  # Garante que o carro comece dentro do limite direito da estrada

        # Ajuste da posição vertical (cima/baixo)
        self.rect.y = max(self.rect.y, 0)  # Garante que o carro não comece fora da tela para cima
        self.rect.y = min(self.rect.y,
                          screen_height - self.rect.height)  # Garante que o carro não comece fora da tela para baixo

    def update(self):

        # Atualiza a posição do jogador com base nas teclas pressionadas, com restrições para não sair da estrada.

        keys = pygame.key.get_pressed()

        # Movimentação horizontal com restrição dentro da estrada
        if keys[pygame.K_LEFT] and self.rect.left > self.road_left:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.road_right:
            self.rect.x += self.speed

        # Movimentação vertical com restrição dentro da tela
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

    def render(self, screen):
        # Desenha a imagem do jogador na tela na posição atual.

        screen.blit(self.image, (self.rect.x, self.rect.y))

    def reset_position(self):
        # Reseta a posição do jogador para a posição inicial.

        # Define a posição inicial do jogador dentro dos limites da estrada
        self.rect.x = self.road_left + (self.road_width - self.rect.width) // 2  # Centraliza o carro dentro da estrada
        self.rect.y = self.screen_height - self.rect.height - 10  # Coloca o carro na parte inferior da tela
