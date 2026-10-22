"""
Cấu hình toàn cục cho trò chơi Obstacle Runner.
Chứa các hằng số về kích thước màn hình, màu sắc, tốc độ và đường dẫn tài nguyên.
"""
import os

# =========================
# KÍCH THƯỚC MÀN HÌNH & FPS
# =========================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# =========================
# BẢNG MÀU CHUẨN
# =========================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 220, 255)
GOLD = (255, 215, 0)
ORANGE = (255, 140, 0)
PURPLE = (180, 80, 255)

# Bảng màu giao diện hiện đại (Modern Cyber / Glassmorphism UI)
UI_BG_OVERLAY = (10, 14, 24, 215)
UI_CARD_BG = (18, 24, 38, 230)
UI_CARD_BORDER = (50, 70, 110)
UI_TEXT_PRIMARY = (255, 255, 255)
UI_TEXT_MUTED = (160, 175, 200)

UI_ACCENT_CYAN = (0, 220, 255)
UI_ACCENT_GREEN = (46, 213, 115)
UI_ACCENT_GOLD = (255, 193, 7)
UI_ACCENT_RED = (255, 71, 87)
UI_ACCENT_PURPLE = (165, 94, 234)

# =========================
# CẤU HÌNH ĐỘ KHÓ BAN ĐẦU
# =========================
DIFFICULTY_SPEEDS = {
    "EASY": 5,
    "MEDIUM": 8,
    "HARD": 11
}

# =========================
# THÔNG SỐ ĐỐI TƯỢNG PLAYER
# =========================
PLAYER_START_X = 370
PLAYER_START_Y = 480
PLAYER_SPEED = 7
PLAYER_MAX_HP = 3
PLAYER_IFRAMES_DURATION = 90  # 1.5 giây tại 60 FPS

# =========================
# THÔNG SỐ CHƯỚNG NGẠI VẬT (OBSTACLES)
# =========================
OBSTACLE_COUNT = 5
SPEED_INCREMENT_SCORE_INTERVAL = 50
SPEED_INCREMENT_AMOUNT = 0.5

# Thiên thạch / Tên lửa rơi nhanh (Meteor)
METEOR_WARNING_DURATION = 70      # ~1.15 giây cảnh báo trước khi lao xuống
METEOR_SPEED_MULTIPLIER = 2.0     # Lao nhanh gấp 2 lần tốc độ cơ bản
METEOR_SPAWN_INTERVAL = (360, 600) # Chu kỳ xuất hiện (khoảng 6 - 10 giây một lần)

# Chướng ngại vật lượn sóng (Wavy)
WAVY_AMPLITUDE_RANGE = (40, 75)
WAVY_FREQUENCY = 0.02

# =========================
# CẤU HÌNH POWER-UPS (VẬT PHẨM)
# =========================
POWERUP_SPAWN_CHANCE = 280  # Xác suất xuất hiện mỗi frame
POWERUP_SPEED = 4
POWERUP_SCORE_BONUS = 2
SLOW_MO_DURATION = 300      # 5 giây tại 60 FPS
SLOW_MO_FACTOR = 0.5        # Giảm 50% tốc độ chướng ngại vật

# =========================
# CẤU HÌNH HIỆU ỨNG NỀN CUỘN
# =========================
BACKGROUND_SCROLL_SPEED = 2.5

# =========================
# ĐƯỜNG DẪN TÀI NGUYÊN (ASSETS)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKGROUND_PATH = os.path.join(BASE_DIR, "background.png")
PLAYER_IMG_PATH = os.path.join(BASE_DIR, "player.png")
OBSTACLE_IMG_PATH = os.path.join(BASE_DIR, "obstacle.png")
HEART_IMG_PATH = os.path.join(BASE_DIR, "heart.png")
