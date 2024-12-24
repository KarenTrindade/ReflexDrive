import pygame
import random


class Bonus:
    BONUS_TYPES = {
        "double": "assets/images/carros/HP_Bonus.png",  # Imagem para o bônus de duplicação de pontuação
        "slow": "assets/images/carros/Jumping_Pad_02.png"  # Imagem para o bônus de desaceleração
    }
    def __init__(self, type, x, y, screen_width, screen_height, speed=2):

        # Inicializa um bônus no jogo.


        self.type = type  # Tipo do bônus
        self.x = x  # Posição X
        self.y = y  # Posição Y
        self.speed = speed  # Velocidade de movimento
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Carrega e redimensiona a imagem do bônus
        self.image = pygame.image.load(self.BONUS_TYPES[type]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        # Define o retângulo para colisão
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, game_speed):
        # Atualiza a posição do bônus com base na velocidade do jogo.
        self.y += self.speed + game_speed  # O bônus move-se com a velocidade do jogo
        self.rect.y = self.y  # Atualiza a posição do retângulo de colisão

    def render(self, screen):
        # Desenha o bônus na tela.
        screen.blit(self.image, self.rect)

    def check_collision(self, player):
        # Verifica colisão com o jogador.
        return self.rect.colliderect(player.rect)

    def apply_bonus(self, obstacles, background):

        # Aplica o efeito do bônus ao fundo e aos obstáculos.

        # :para obstacles: Lista de obstáculos no jogo.
        # :para background: Instância do fundo do jogo.

        if self.type == "double":
            # Multiplica a pontuação em uma classe externa (como GameManager)
            return "double"  # Retorna um sinalizador para o GameManager
        elif self.type == "slow":
            # Desacelera a velocidade dos obstáculos
            for obstacle in obstacles:
                obstacle.speed = max(obstacle.speed - 1, 1)  # Garante que a velocidade mínima seja 1
            # Desacelera a velocidade do fundo
            background.speed = max(background.speed - 1, 1)

    def is_off_screen(self):
        # Verifica se o bônus saiu da tela.
        return self.y > self.screen_height


# Função auxiliar para criar bônus aleatórios
def create_random_bonus(screen_width, screen_height, road_x_min, road_x_max):
    # Cria um bônus em uma posição aleatória restrita à área da estrada.

    # :param screen_width: Largura da tela.
    # :param screen_height: Altura da tela.
    # :param road_x_min: Limite mínimo X da estrada.
    # :param road_x_max: Limite máximo X da estrada.

    type = random.choice(list(Bonus.BONUS_TYPES.keys()))  # Escolhe um tipo aleatório
    x_position = random.randint(road_x_min, road_x_max - 50)  # Restrito à estrada
    y_position = random.randint(-200, -50)  # Aparecem acima da tela
    return Bonus(type, x_position, y_position, screen_width, screen_height)
