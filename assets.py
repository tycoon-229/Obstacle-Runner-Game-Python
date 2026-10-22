"""
Quản lý việc tải và scale hình ảnh, font chữ cho trò chơi.
Tránh việc nạp tài nguyên nhiều lần gây lãng phí bộ nhớ.
"""
import pygame
from config import (
    BACKGROUND_PATH,
    PLAYER_IMG_PATH,
    OBSTACLE_IMG_PATH,
    HEART_IMG_PATH,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def load_assets(self):
        if self.initialized:
            return

        # Load hình ảnh
        raw_bg = pygame.image.load(BACKGROUND_PATH)
        self.background = pygame.transform.scale(raw_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

        raw_player = pygame.image.load(PLAYER_IMG_PATH)
        self.player_img = pygame.transform.scale(raw_player, (70, 90))

        raw_obstacle = pygame.image.load(OBSTACLE_IMG_PATH)
        self.obstacle_img = pygame.transform.scale(raw_obstacle, (70, 90))

        raw_heart = pygame.image.load(HEART_IMG_PATH)
        self.heart_img = pygame.transform.scale(raw_heart, (32, 32))

        # Biến thể màu cho chướng ngại vật lượn sóng (Tím/Hồng năng lượng)
        wavy = self.obstacle_img.copy()
        tint_wavy = pygame.Surface(wavy.get_size(), pygame.SRCALPHA)
        tint_wavy.fill((160, 60, 255, 95))
        wavy.blit(tint_wavy, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.wavy_obstacle_img = wavy

        # Biến thể màu cho thiên thạch / tên lửa rơi nhanh (Đỏ lửa rực cháy)
        meteor = self.obstacle_img.copy()
        tint_meteor = pygame.Surface(meteor.get_size(), pygame.SRCALPHA)
        tint_meteor.fill((255, 50, 0, 115))
        meteor.blit(tint_meteor, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.meteor_img = meteor

        # Danh sách font hiện đại ưu tiên Segoe UI, Trebuchet MS, Arial
        preferred_fonts = ["segoeui", "trebuchetms", "verdana", "arial"]

        self.title_font = pygame.font.SysFont(preferred_fonts, 58, bold=True)
        self.header_font = pygame.font.SysFont(preferred_fonts, 36, bold=True)
        self.button_font = pygame.font.SysFont(preferred_fonts, 24, bold=True)
        self.hud_font = pygame.font.SysFont(preferred_fonts, 20, bold=True)
        self.number_font = pygame.font.SysFont(preferred_fonts, 26, bold=True)
        self.badge_font = pygame.font.SysFont(preferred_fonts, 15, bold=True)
        self.warning_font = pygame.font.SysFont(["segoeui", "arial"], 42, bold=True)

        # Giữ bí danh tương thích ngược
        self.big_font = self.title_font
        self.medium_font = self.header_font
        self.small_font = self.hud_font

        self.initialized = True

assets = AssetManager()
