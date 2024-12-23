# config.py
WIDTH, HEIGHT = 800, 600

# Pode fazer esse ajuste para mim?:
#
# def update(self):
#         """Atualiza as posições para simular movimento."""
#         # Atualizar posições da grama
#         new_grass_positions = []
#         for x, y in self.grass_positions:
#             y += self.grass_speed
#             if y >= self.screen_height:
#                 y = -self.screen_height // 2  # Reinicia a posição da grama acima da tela
#             new_grass_positions.append((x, y))
#         self.grass_positions = new_grass_positions
#
#         # Atualizar posições das estradas
#         for i in range(len(self.positions)):
#             self.positions[i] += self.scroll_speed
#             if self.positions[i] >= self.screen_height:
#                 self.positions[i] -= self.screen_height * len(self.road_images)
