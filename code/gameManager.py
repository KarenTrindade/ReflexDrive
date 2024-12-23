import pygame
import random
from config import WIDTH, HEIGHT
from code.player import Player
from code.background import Background
from code.obstacle import Obstacle, create_random_obstacle
from code.bonus import Bonus

class GameManager:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu
        self.player = Player(x=WIDTH // 2, y=HEIGHT - 100, speed=5, screen_width=WIDTH, screen_height=HEIGHT)

        self.background = Background(
            road_images=["assets/images/carros/Road_Main.png", "assets/images/carros/Road_Main_1.png"],
            grass_image="assets/images/backgrounds/Grass_Tile.png",
            scroll_speed=2,
            screen_width=WIDTH,
            screen_height=HEIGHT
        )

        self.obstacles = []
        self.bonuses = []
        self.existing_objects = []
        self.score = 0
        self.game_over = False
        self.current_state = "menu"

        self.bonus_spawn_time = 0
        self.game_speed = 1.5
        self.speed_increase_rate = 0.005
        self.max_game_speed = 7

        self.is_slowed = False
        self.slow_end_time = 0

        # Adicionar sons
        pygame.mixer.init()
        self.game_music = "assets/sounds/Game.mp3"
    def play_game_music(self):
        # Toca o som de fundo do jogo.
        pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Toca em loop

    def stop_music(self):
        # Para qualquer música que esteja tocando.
        pygame.mixer.music.stop()
    def increase_game_speed(self):
        # Aumenta a velocidade do jogo gradualmente.
        if not self.is_slowed:
            self.game_speed += self.speed_increase_rate
            self.game_speed = min(self.game_speed, self.max_game_speed)  # Limita a velocidade máxima

    def apply_slow_bonus(self, duration):
        # Aplica o efeito de desaceleração temporária.
        self.is_slowed = True
        self.slow_end_time = pygame.time.get_ticks() + duration
        self.game_speed = max(1, self.game_speed * 0.5)  # Reduz a velocidade pela metade, com limite mínimo de 1

    def update_game_speed(self):
        # Atualiza a velocidade do jogo, verificando se o efeito de desaceleração terminou.
        if self.is_slowed and pygame.time.get_ticks() > self.slow_end_time:
            self.is_slowed = False
        self.increase_game_speed()

    def apply_bonus(self, bonus):
        # Aplica o efeito de um bônus ao jogador.
        if bonus.type == "slow":
            self.apply_slow_bonus(duration=5000)  # 5 segundos de efeito
        elif bonus.type == "double":
            self.score += 2  # Adiciona 2 pontos como bônus

    def spawn_obstacles_and_bonuses(self):
        """Lógica para spawnar obstáculos e bônus periodicamente."""
        # Só gera bônus se o jogo não tiver acabado
        if self.game_over:
            return

        road_x_min = WIDTH // 4  # Define os limites laterais da estrada
        road_x_max = (WIDTH // 4) * 3

        # Cria obstáculos aleatórios na estrada
        if len(self.obstacles) < 2:  # Limite de obstáculos na tela
            obstacle = self.create_non_overlapping_object(create_random_obstacle, WIDTH, HEIGHT, road_x_min, road_x_max)
            obstacle.y = random.randint(-400, -100)
            self.obstacles.append(obstacle)

        # Cria bônus aleatórios na tela
        current_time = pygame.time.get_ticks()
        if current_time - self.bonus_spawn_time > 3000:  # 3 segundos entre bônus
            def create_bonus():
                x_position = random.randint(WIDTH // 4, (WIDTH // 4) * 3 - 50)
                y_position = random.randint(-400, -100)
                return Bonus(type=random.choice(["double", "slow"]), x=x_position, y=y_position,
                             screen_width=WIDTH, screen_height=HEIGHT)

            bonus = self.create_non_overlapping_object(create_bonus)
            self.bonuses.append(bonus)
            self.bonus_spawn_time = current_time

    def run_game(self):
        # Lógica principal do jogo.
        if not self.game_over:
            self.update_game_speed()  # Atualiza a velocidade global
            self.spawn_obstacles_and_bonuses()

            # Atualiza e renderiza o background
            self.background.update()
            self.background.render(self.screen)

            # Atualiza e desenha o jogador
            self.player.update()
            self.player.render(self.screen)

            # Atualiza, desenha e remove obstáculos
            for obstacle in self.obstacles[:]:
                if obstacle.update(self.game_speed):
                    self.obstacles.remove(obstacle)
                    self.existing_objects.remove(obstacle)
                    self.score += 1

                obstacle.render(self.screen)

                # Verifica colisão com o jogador
                if obstacle.check_collision(self.player):
                    self.game_over = True
                    self.current_state = "fim"  # Altera o estado para "fim" quando houver colisão
                    self.render_game_over_screen()
                    break

            # Atualiza, desenha e remove bônus
            if not self.game_over:
                for bonus in self.bonuses[:]:
                    if bonus.update(self.game_speed):
                        self.bonuses.remove(bonus)
                        self.existing_objects.remove(bonus)

                    bonus.render(self.screen)
                    if bonus.check_collision(self.player):
                        self.apply_bonus(bonus)
                        self.bonuses.remove(bonus)
                        self.existing_objects.remove(bonus)

            # Exibe a pontuação
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))

            # Atualiza a tela
            pygame.display.flip()

        elif self.game_over:  # Renderiza a tela de Game Over
            self.render_game_over_screen()

    def render_game_over_screen(self):
        # Renderiza a tela de Game Over com imagem, texto e pontuação final.

        # Tocar música de fundo para a tela de Game Over
        pygame.mixer.music.load("assets/sounds/GameOver.mp3")
        pygame.mixer.music.set_volume(0.5)  # Define o volume da música
        pygame.mixer.music.play(-1)  # Toca a música em loop

        # Imagem de fundo para a tela de Game Over
        game_over_image = pygame.image.load("assets/images/backgrounds/Water_Tile.png")
        game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))

        # Preenche toda a tela com a imagem de fundo
        self.screen.blit(game_over_image, (0, 0))

        # Texto "Game Over"
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        # Pontuação final
        font = pygame.font.Font(None, 36)
        final_score_text = font.render(f"Pontuação Final: {self.score}", True, (255, 255, 255))
        self.screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2))

        # Instrução para reiniciar ou voltar ao menu
        instruction_text = font.render("Pressione Enter para reiniciar ou ESC para voltar ao menu", True,
                                       (255, 255, 255))
        self.screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 1.5))

        # Atualiza a tela
        pygame.display.flip()

    def create_non_overlapping_object(self, create_function, *args):
        # Cria um objeto (obstáculo ou bônus) que não se sobrepõe a objetos existentes.

        max_attempts = 10  # Limite de tentativas para evitar sobreposição
        for _ in range(max_attempts):
            new_object = create_function(*args)
            if not any(new_object.rect.colliderect(obj.rect) for obj in self.existing_objects):
                self.existing_objects.append(new_object)  # Adiciona à lista de objetos existentes
                return new_object
        raise RuntimeError("Não foi possível criar um objeto sem sobreposição.")

    def handle_events(self):
        # Gerencia os eventos do jogo.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if self.current_state == "menu":
                    result = self.menu.handle_input(event)
                    if result == "jogo":
                        self.current_state = "jogo"
                        self.game_over = False
                        self.score = 0  # Reinicia pontuação

                        # Troca para o som do jogo
                        self.stop_music()  # Para o som do menu
                        self.play_game_music()

                    elif result == "sair":
                        pygame.quit()
                        exit()
                elif self.current_state == "jogo" and event.key == pygame.K_ESCAPE:
                    self.current_state = "menu"
                    self.stop_music()  # Para o som do jogo
                elif self.current_state == "fim":
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.current_state = "menu"
                        self.stop_music()  # Para o som do fim e volta ao menu

    def reset_game(self):
        # Reinicia o estado do jogo.
        self.game_over = False
        self.current_state = "jogo"
        self.score = 0
        self.obstacles.clear()
        self.bonuses.clear()
        self.existing_objects.clear()
        self.player.reset_position()
        self.game_speed = 1.5

        self.stop_music()  # Garante que o som antigo pare
        self.play_game_music()  # Reinicia o som do jogo

    def update(self):
        # Atualiza o estado do jogo.
        self.handle_events()

        if self.current_state == "menu":
            self.menu.render_menu()
        elif self.current_state == "jogo":
            self.run_game()
