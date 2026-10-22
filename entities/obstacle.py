import math
import random
import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    RED,
    YELLOW,
    ORANGE,
    WHITE,
    WAVY_AMPLITUDE_RANGE,
    WAVY_FREQUENCY,
    METEOR_WARNING_DURATION,
    METEOR_SPEED_MULTIPLIER
)
from assets import assets

class Obstacle(pygame.sprite.Sprite):
    """
    Chướng ngại vật tiêu chuẩn.
    Có khả năng chuyển đổi giữa rơi thẳng (Normal) và lượn sóng (Wavy) theo hàm sin.
    Sử dụng pygame.mask để xử lý va chạm chính xác theo từng pixel (Pixel-perfect Hitbox).
    """
    def __init__(self, image, current_speed, is_wavy=False):
        super().__init__()
        self.normal_image = image
        self.is_wavy = is_wavy
        self.speed_y = current_speed

        self.amplitude = random.randint(*WAVY_AMPLITUDE_RANGE)
        self.frequency = WAVY_FREQUENCY
        self.base_x = float(random.randint(80, SCREEN_WIDTH - 150))
        self.y_float = float(random.randint(-700, -100))

        self._setup_sprite()

    def _setup_sprite(self):
        if self.is_wavy:
            self.image = assets.wavy_obstacle_img
        else:
            self.image = self.normal_image

        self.rect = self.image.get_rect()
        self.rect.x = int(self.base_x)
        self.rect.y = int(self.y_float)
        # Khởi tạo mask pixel-perfect
        self.mask = pygame.mask.from_surface(self.image)

    def reset_position(self):
        """Reset lại vị trí khi rơi qua đáy màn hình và ngẫu nhiên chọn lại dạng rơi."""
        # 35% khả năng biến thành chướng ngại vật lượn sóng
        self.is_wavy = (random.random() < 0.35)
        self.amplitude = random.randint(*WAVY_AMPLITUDE_RANGE)
        self.frequency = WAVY_FREQUENCY
        self.base_x = float(random.randint(80, SCREEN_WIDTH - 150))
        self.y_float = float(random.randint(-500, -100))
        self._setup_sprite()

    def update(self):
        self.y_float += self.speed_y
        self.rect.y = int(self.y_float)

        if self.is_wavy:
            # Di chuyển tọa độ X theo hàm sin(y)
            offset_x = math.sin(self.y_float * self.frequency) * self.amplitude
            new_x = self.base_x + offset_x
            # Giới hạn trong phạm vi màn hình
            new_x = max(10, min(SCREEN_WIDTH - 80, new_x))
            self.rect.x = int(new_x)

        # Khi rơi qua mép dưới màn hình
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            return True
        return False


class FastMeteor(pygame.sprite.Sprite):
    """
    Thiên thạch / Tên lửa rơi cực nhanh.
    Có thời gian cảnh báo trước bằng biểu tượng dấu chấm than [ ! ] nhấp nháy
    và tia laser cảnh báo làn đường rơi ở mép trên màn hình.
    """
    def __init__(self, current_speed):
        super().__init__()
        self.image = assets.meteor_img
        self.rect = self.image.get_rect()

        # Chọn làn đường xuất hiện ngẫu nhiên
        self.target_x = random.randint(40, SCREEN_WIDTH - 110)
        self.rect.x = self.target_x
        self.rect.y = -300  # Giấu trên trời trong lúc cảnh báo

        self.mask = pygame.mask.from_surface(self.image)
        self.base_speed = current_speed
        self.speed_y = current_speed * METEOR_SPEED_MULTIPLIER + 3.0

        # Trạng thái cảnh báo
        self.is_warning = True
        self.warning_timer = METEOR_WARNING_DURATION
        self.tick_counter = 0

    def update(self, current_speed=None):
        self.tick_counter += 1

        if current_speed is not None:
            self.speed_y = current_speed * METEOR_SPEED_MULTIPLIER + 3.0

        if self.is_warning:
            self.warning_timer -= 1
            if self.warning_timer <= 0:
                self.is_warning = False
                self.rect.y = -90  # Bắt đầu lao xuống từ trên mép màn hình
            return False
        else:
            self.rect.y += int(self.speed_y)
            # Khi rơi qua đáy màn hình thì tự hủy
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
                return True
            return False

    def draw_warning(self, screen):
        """Vẽ biểu tượng cảnh báo dấu chấm than [ ! ] nhấp nháy và dải tia laser trên màn hình."""
        if not self.is_warning:
            return

        box_width = 46
        box_height = 42
        box_x = self.target_x + (self.rect.width - box_width) // 2
        box_y = 12

        # 1. Tia laser cảnh báo mờ mờ chiếu dọc toàn bộ làn rơi
        laser_surface = pygame.Surface((box_width, SCREEN_HEIGHT), pygame.SRCALPHA)
        laser_alpha = 40 if self.tick_counter % 12 < 6 else 75
        laser_surface.fill((255, 0, 0, laser_alpha))
        screen.blit(laser_surface, (box_x, 0))

        # 2. Hộp cảnh báo nhấp nháy màu đỏ / vàng
        flash_color = RED if self.tick_counter % 14 < 7 else YELLOW
        pygame.draw.rect(screen, (30, 0, 0), (box_x - 2, box_y - 2, box_width + 4, box_height + 4), border_radius=6)
        pygame.draw.rect(screen, flash_color, (box_x, box_y, box_width, box_height), width=3, border_radius=5)

        # 3. Ký tự dấu chấm than '!'
        warn_char = assets.warning_font.render("!", True, flash_color)
        char_rect = warn_char.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
        screen.blit(warn_char, char_rect)

    def draw_trail(self, screen):
        """Vẽ vệt lửa rực cháy phía sau thiên thạch khi đang lao xuống."""
        if self.is_warning or self.rect.y < -50:
            return

        tail_x = self.rect.centerx
        tail_top = self.rect.top
        tail_length = min(70, int(self.speed_y * 4))

        # Ngọn lửa ngoài (Cam/Đỏ)
        flame_outer = [
            (tail_x - 14, tail_top + 10),
            (tail_x + 14, tail_top + 10),
            (tail_x, tail_top - tail_length)
        ]
        pygame.draw.polygon(screen, ORANGE, flame_outer)

        # Lõi lửa trong (Vàng/Trắng)
        flame_inner = [
            (tail_x - 7, tail_top + 8),
            (tail_x + 7, tail_top + 8),
            (tail_x, tail_top - tail_length * 0.6)
        ]
        pygame.draw.polygon(screen, YELLOW, flame_inner)
