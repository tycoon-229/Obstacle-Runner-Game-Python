import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN, CYAN, GOLD, WHITE, POWERUP_SPEED

class PowerUp(pygame.sprite.Sprite):
    TYPE_HEAL = "HEAL"
    TYPE_SHIELD = "SHIELD"
    TYPE_SLOW_MO = "SLOW_MO"

    def __init__(self, power_type=None):
        super().__init__()

        # Nếu không chỉ định trước thì chọn ngẫu nhiên loại vật phẩm
        # Tỉ lệ: 45% Hồi máu, 35% Khiên, 20% Làm chậm thời gian
        if power_type is None:
            self.power_type = random.choices(
                [self.TYPE_HEAL, self.TYPE_SHIELD, self.TYPE_SLOW_MO],
                weights=[45, 35, 20]
            )[0]
        else:
            self.power_type = power_type

        self.size = 38
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self._render_icon()

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.size)
        self.rect.y = random.randint(-800, -100)
        self.speed_y = POWERUP_SPEED
        self.mask = pygame.mask.from_surface(self.image)

    def _render_icon(self):
        """Vẽ biểu tượng trực quan riêng biệt cho từng loại vật phẩm."""
        center = self.size // 2
        radius = self.size // 2

        if self.power_type == self.TYPE_HEAL:
            # Nền tròn xanh lá + Dấu cộng y tế màu trắng
            pygame.draw.circle(self.image, GREEN, (center, center), radius)
            pygame.draw.circle(self.image, WHITE, (center, center), radius, 2)
            # Dấu cộng trắng
            pygame.draw.rect(self.image, WHITE, (center - 3, center - 10, 6, 20), border_radius=2)
            pygame.draw.rect(self.image, WHITE, (center - 10, center - 3, 20, 6), border_radius=2)

        elif self.power_type == self.TYPE_SHIELD:
            # Nền tròn xanh cyan + Khiên bảo hộ
            pygame.draw.circle(self.image, CYAN, (center, center), radius)
            pygame.draw.circle(self.image, WHITE, (center, center), radius, 2)
            # Biểu tượng hình khiên
            points = [
                (center, center - 10),
                (center + 9, center - 6),
                (center + 7, center + 4),
                (center, center + 11),
                (center - 7, center + 4),
                (center - 9, center - 6),
            ]
            pygame.draw.polygon(self.image, WHITE, points)

        elif self.power_type == self.TYPE_SLOW_MO:
            # Nền tròn màu vàng kim + Ký hiệu đồng hồ
            pygame.draw.circle(self.image, GOLD, (center, center), radius)
            pygame.draw.circle(self.image, WHITE, (center, center), radius, 2)
            # Vòng kim đồng hồ bên trong
            pygame.draw.circle(self.image, (40, 40, 40), (center, center), radius - 6)
            # Kim chỉ giờ và phút
            pygame.draw.line(self.image, WHITE, (center, center), (center, center - 7), 2)
            pygame.draw.line(self.image, WHITE, (center, center), (center + 6, center), 2)

    def update(self):
        self.rect.y += self.speed_y

        # Tự hủy biến mất khỏi bộ nhớ khi rơi ra khỏi màn hình
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
