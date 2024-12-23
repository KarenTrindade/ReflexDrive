#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame
import random


class Obstacle:
    _images = {
        "car": None,
        "car2": None,
    }

    def __init__(self, type, x, y, screen_width, screen_height, speed=2, scale_factors=None):
        """
        Inicializa um obstáculo com tipo, posição, velocidade e redimensionamento de imagem.

        :param type: Tipo do obstáculo (ex: "car" ou "cone").
        :param x: Posição inicial do obstáculo no eixo X.
        :param y: Posição inicial do obstáculo no eixo Y.
        :param screen_width: Largura da tela (não usado diretamente, mas necessário para instância futura).
        :param screen_height: Altura da tela para controle de remoção.
        :param speed: Velocidade de movimento do obstáculo (padrão: 2).
        :param scale_factors: Dicionário com fatores de escala para os tipos de obstáculos.
        """
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
        """
        Atualiza a posição do obstáculo e verifica se ele saiu da tela.

        :param game_speed: Velocidade global do jogo que afeta o movimento do obstáculo.
        :return: True se o obstáculo saiu da tela; caso contrário, False.
        """
        self.y += self.speed + game_speed  # Movimenta o obstáculo com base na velocidade do jogo
        self.rect.y = self.y
        return self.y > self.screen_height

    def render(self, screen):
        """
        Desenha o obstáculo na tela.

        :param screen: Superfície de exibição do jogo.
        """
        screen.blit(self.image, self.rect)

    def check_collision(self, player):
        """
        Verifica a colisão entre o obstáculo e o jogador.

        :param player: Objeto do jogador.
        :return: True se houver colisão; caso contrário, False.
        """
        return self.rect.colliderect(player.rect)


def create_random_obstacle(screen_width, screen_height, road_x_min, road_x_max):
    """
    Cria um obstáculo em uma posição aleatória restrita à área da estrada.

    :param screen_width: Largura da tela.
    :param screen_height: Altura da tela.
    :param road_x_min: Limite mínimo X da estrada.
    :param road_x_max: Limite máximo X da estrada.
    :return: Instância da classe Obstacle.
    """
    # Escolhe aleatoriamente o tipo de obstáculo
    obstacle_type = random.choice(["car", "car2"])

    # Define uma posição aleatória dentro da faixa da estrada
    x_position = random.randint(road_x_min, road_x_max - 50)
    y_position = random.randint(-200, -50)  # Começa fora da tela, acima

    return Obstacle(obstacle_type, x_position, y_position, screen_width, screen_height)
