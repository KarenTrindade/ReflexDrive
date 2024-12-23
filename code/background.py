import pygame


class Background:
    def __init__(self, road_images, grass_image, scroll_speed, screen_width, screen_height):
        """Inicializa o fundo do jogo com imagens de estrada e grama."""
        try:
            # Carregar a imagem de grama
            grass = pygame.image.load(grass_image).convert_alpha()
            # Calcular a nova largura da grama para cobrir a tela
            grass_width = screen_width
            # Manter a proporção original da imagem
            aspect_ratio = grass.get_width() / grass.get_height()
            grass_height = int(grass_width / aspect_ratio)
            # Redimensionar a imagem de grama
            self.grass_piece = pygame.transform.scale(grass, (grass_width, grass_height))
        except pygame.error as e:
            raise ValueError(f"Erro ao carregar a imagem de grama: {e}")

        # Criar posições para a grade de grama (2x1)
        self.initial_grass_positions = [
            (0, 0), (0, screen_height)
        ]
        self.grass_positions = self.initial_grass_positions.copy()

        # Inicializar velocidades de rolagem
        self.grass_speed = scroll_speed
        self.scroll_speed = scroll_speed

        # Dimensões da tela
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Carregar e redimensionar as imagens de estrada
        self.road_images = []
        for image_path in road_images:
            try:
                image = pygame.image.load(image_path).convert_alpha()
                road_width = int(screen_width * 0.6)
                road_height = screen_height
                image = pygame.transform.scale(image, (road_width, road_height))
                self.road_images.append(image)
            except pygame.error as e:
                print(f"Erro ao carregar a imagem de estrada {image_path}: {e}")
                continue

        if not self.road_images:
            raise ValueError("Nenhuma imagem de estrada válida foi carregada.")

        # Posições iniciais das imagens de estrada
        self.initial_positions = [i * -screen_height for i in range(len(self.road_images))]
        self.positions = self.initial_positions.copy()

    def reset(self):
        #3Reinicia as posições e velocidades do fundo.
        self.grass_positions = self.initial_grass_positions.copy()
        self.positions = self.initial_positions.copy()
        self.grass_speed = self.scroll_speed

    def set_scroll_speed(self, speed):
        # Ajusta a velocidade de rolagem.
        self.scroll_speed = speed
        self.grass_speed = speed

    def update(self):
        # Atualizar posições da grama
        new_grass_positions = []
        for x, y in self.grass_positions:
            y += self.grass_speed
            if y >= self.screen_height:
                y = -self.grass_piece.get_height()  # Reinicia a posição da grama acima da tela
            new_grass_positions.append((x, y))
        self.grass_positions = new_grass_positions

        # Atualizar posições das estradas
        for i in range(len(self.positions)):
            self.positions[i] += self.scroll_speed
            if self.positions[i] >= self.screen_height:
                self.positions[i] -= self.screen_height * len(self.road_images)

    def render(self, screen):
        # Renderizar a grade de grama
        for x, y in self.grass_positions:
            screen.blit(self.grass_piece, (x, y))

        # Renderizar as imagens de estrada centralizadas
        for i, image in enumerate(self.road_images):
            road_x = (self.screen_width - image.get_width()) // 2  # Centraliza horizontalmente
            screen.blit(image, (road_x, self.positions[i]))
