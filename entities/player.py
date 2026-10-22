import math
import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    PLAYER_MAX_HP,
    PLAYER_IFRAMES_DURATION,
    CYAN,
    WHITE
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Di chuyển tự do 4 hướng (X và Y)
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed = PLAYER_SPEED

        # Pixel-perfect Mask cho va chạm chính xác
        self.mask = pygame.mask.from_surface(self.image)

        # Hệ thống HP & Bất tử tạm thời
        self.hp = PLAYER_MAX_HP
        self.invincible = False
        self.invincible_timer = 0

        # Hệ thống Khiên bảo vệ (Shield)
        self.has_shield = False
        self.shield_anim_tick = 0

    def update(self):
        # Cập nhật vị trí tự do theo cả trục X và trục Y
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Giới hạn nhân vật không bay ra ngoài màn hình (Trục X)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Giới hạn nhân vật không bay ra ngoài màn hình (Trục Y)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        # Xử lý thời gian tàng hình (I-frames)
        if self.invincible:
            self.invincible_timer -= 1

            # Tạo hiệu ứng nhấp nháy bằng độ trong suốt (alpha)
            if self.invincible_timer % 10 < 5:
                self.image.set_alpha(0)    # Ẩn
            else:
                self.image.set_alpha(255)  # Hiện

            # Hết thời gian tàng hình
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image.set_alpha(255)

        # Hiệu ứng nhịp đập khiên
        if self.has_shield:
            self.shield_anim_tick += 1

    def take_damage(self):
        """
        Xử lý khi va chạm chướng ngại vật:
        - Nếu có Khiên: Phá hủy khiên, không mất HP, kích hoạt I-frame ngắn. Trả về 'SHIELD_BROKEN'.
        - Nếu không có Khiên và không trong I-frame: Trừ 1 HP, kích hoạt I-frame đầy đủ. Trả về 'DAMAGED'.
        - Nếu đang trong I-frame: Trả về False.
        """
        if self.invincible:
            return False

        if self.has_shield:
            self.has_shield = False
            self.invincible = True
            self.invincible_timer = 60  # 1 giây an toàn sau khi khiên vỡ
            return "SHIELD_BROKEN"

        self.hp -= 1
        self.invincible = True
        self.invincible_timer = PLAYER_IFRAMES_DURATION
        return "DAMAGED"

    def draw_effects(self, screen):
        """Vẽ hiệu ứng vòng hào quang năng lượng khi có Khiên (Shield)."""
        if self.has_shield and not (self.invincible and self.invincible_timer % 10 < 5):
            pulse = math.sin(self.shield_anim_tick * 0.15) * 3
            center_x = self.rect.centerx
            center_y = self.rect.centery
            shield_rect = pygame.Rect(
                self.rect.left - 8 - pulse,
                self.rect.top - 8 - pulse,
                self.rect.width + 16 + pulse * 2,
                self.rect.height + 16 + pulse * 2
            )
            pygame.draw.ellipse(screen, CYAN, shield_rect, width=3)
            pygame.draw.ellipse(screen, WHITE, shield_rect.inflate(-4, -4), width=1)
