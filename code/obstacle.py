import pygame
import random


class Obstacle:
    _images = {
        "car": None,
        "car2": None,
    }

    def __init__(self, type, x, y, screen_width, screen_height, speed=2, scale_factors=None):
        # Inicializa um obstáculo com tipo, posição, velocidade e redimensionamento de imagem.

        self.type = type
        self.x = x
        self.y = y
        self.speed = speed
        self.screen_height = screen_height

        # Configurar os fatores de escala padrão, se não fornecido
        scale_factors = scale_factors or {"car": 0.10, "car2": 0.11}

        # Carregar e redimensionar imagem do obstáculo
        if Obstacle._images[type] is None:
            if type == "car":
                image_path = "assets/images/carros/Car_2_001.png"
            elif type == "car2":
                image_path = "assets/images/carros/Car_3_01.png"
            else:
                raise ValueError(f"Tipo de obstáculo '{type}' não reconhecido.")

            original_image = pygame.image.load(image_path)
            scale_factor = scale_factors.get(type, 0.10)
            Obstacle._images[type] = pygame.transform.scale(
                original_image,
                (int(original_image.get_width() * scale_factor),
                 int(original_image.get_height() * scale_factor))
            )
        self.image = Obstacle._images[type]

        # Define o retângulo de colisão com base na posição inicial
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self, game_speed):

        # Atualiza a posição do obstáculo e verifica se ele saiu da tela.

        self.y += self.speed + game_speed  # Movimenta o obstáculo com base na velocidade do jogo
        self.rect.y = self.y
        return self.y > self.screen_height

    def render(self, screen):

        # Desenha o obstáculo na tela.

        screen.blit(self.image, self.rect)

    def check_collision(self, player):
        # Verifica a colisão entre o obstáculo e o jogador.

        return self.rect.colliderect(player.rect)


def create_random_obstacle(screen_width, screen_height, road_x_min, road_x_max):
    # Cria um obstáculo em uma posição aleatória restrita à área da estrada.

    # Escolhe aleatoriamente o tipo de obstáculo
    obstacle_type = random.choice(["car", "car2"])

    # Define uma posição aleatória dentro da faixa da estrada
    x_position = random.randint(road_x_min, road_x_max - 50)
    y_position = random.randint(-200, -50)  # Começa fora da tela, acima

    return Obstacle(obstacle_type, x_position, y_position, screen_width, screen_height)
