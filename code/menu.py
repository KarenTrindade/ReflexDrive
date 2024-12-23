import pygame
from config import WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.background_images = [
            pygame.image.load("assets/images/backgrounds/menu_1.png").convert_alpha(),
            pygame.image.load("assets/images/backgrounds/menu_2.png").convert_alpha(),
            pygame.image.load("assets/images/backgrounds/menu_3.png").convert_alpha(),
            pygame.image.load("assets/images/backgrounds/menu_4.png").convert_alpha()
        ]
        self.font = pygame.font.SysFont("bahnschrift", 55, bold=True)
        self.options = ["Iniciar", "Sair"]
        self.selected_option = 0

        # Carrega a imagem central (96x96)
        self.center_image = pygame.image.load("assets/images/backgrounds/Road_Side_02.png").convert_alpha()
        self.center_image = pygame.transform.scale(self.center_image, (96, 96))
        self.center_image_rect = self.center_image.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)  # Centraliza no meio da tela
        )

        # Adiciona o som de fundo do menu
        pygame.mixer.music.load("assets/sounds/Menu.mp3")
        pygame.mixer.music.set_volume(0.5)  # Define o volume


    def render_background(self):
        # Renderiza o fundo com imagens organizadas como um quebra-cabeça.
        positions = [
            (0, 0),  # Posição para part1.png
            (400, 0),  # Posição para part2.png
            (0, 300),  # Posição para part3.png
            (400, 300)  # Posição para part4.png
        ]

        image_width, image_height = 400, 300
        for img, pos in zip(self.background_images, positions):
            scaled_img = pygame.transform.scale(img, (image_width, image_height))
            self.screen.blit(scaled_img, pos)

    def render_menu(self):
        # Renderiza o menu com a imagem central, título em gradiente e opções de texto.
        # Tocar música de fundo se ainda não estiver tocando
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)  # Loop infinito

        self.render_background()

        # Calcular a posição da imagem central
        center_x = WIDTH // 2 - self.center_image.get_width() // 2
        center_y = HEIGHT // 2 - self.center_image.get_height() // 2

        # Criar fonte para o título usando fonte padrão do sistema
        title_font = pygame.font.SysFont("bahnschrift", 80, bold=True)

        # Gerar o texto "Reflex Drive" com gradiente
        title_surface = self.create_text_gradient(
            "Reflex Drive", title_font, (50, 205, 50), (255, 215, 0)
        )
        title_x = WIDTH // 2 - title_surface.get_width() // 2
        title_y = center_y - 120  # Posicionar acima da imagem central

        # Desenhar o título na tela
        self.screen.blit(title_surface, (title_x, title_y))

        # Renderizar a imagem central no meio da tela
        self.screen.blit(self.center_image, (center_x, center_y))

        # Renderizar o texto do menu abaixo da imagem central
        for index, option in enumerate(self.options):
            color = (255, 255, 0) if index == self.selected_option else (255, 255, 255)
            option_text = self.font.render(option, True, color)

            # Calcular a posição do texto para ficar sobre a imagem
            text_x = WIDTH // 2 - option_text.get_width() // 2
            text_y = center_y + 120 + index * 50  # Espaçamento vertical para cada opção (120px abaixo da imagem)

            self.screen.blit(option_text, (text_x, text_y))

    def create_text_gradient(self, text, font, color_top, color_bottom):

        # Cria um texto com gradiente de cor.

        # Renderizar o texto com cor sólida apenas para pegar as dimensões
        text_surface = font.render(text, True, (255, 255, 255))
        width, height = text_surface.get_size()

        # Criar uma superfície transparente
        gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Aplicar gradiente na superfície
        for y in range(height):
            r = color_top[0] + (color_bottom[0] - color_top[0]) * y // height
            g = color_top[1] + (color_bottom[1] - color_top[1]) * y // height
            b = color_top[2] + (color_bottom[2] - color_top[2]) * y // height
            pygame.draw.line(gradient_surface, (r, g, b, 255), (0, y), (width, y))

        # "Recortar" o gradiente no formato do texto
        gradient_surface.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        return gradient_surface

    def handle_input(self, event):
        # Lida com a entrada do usuário para navegação no menu.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.options[self.selected_option] == "Iniciar":
                    pygame.mixer.music.stop()  # Para a música ao iniciar o jogo
                    return "jogo"  # Troca para o estado do jogo
                elif self.options[self.selected_option] == "Sair":
                    pygame.mixer.music.stop()  # Para a música ao sair
                    pygame.quit()
                    exit()
        return "menu"  # Retorna ao menu
