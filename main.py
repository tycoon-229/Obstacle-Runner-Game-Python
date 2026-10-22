"""
File điều phối chính của game Obstacle Runner.
Khởi tạo Pygame, âm thanh, bộ điều phối độ phân giải màn hình (DisplayManager)
và State Machine chuyển đổi giữa các màn hình.
"""
import sys
import pygame
from config import DIFFICULTY_SPEEDS
from assets import assets
from utils import sound_manager, display_manager
from scenes import MainMenu, DifficultyMenu, GameScene, GameOverScene

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Khởi tạo bộ hiển thị ảo (cho phép phóng to, đổi độ phân giải và Fullscreen F11)
    display_manager.init()

    # Khởi tạo bộ âm thanh SFX và BGM
    sound_manager.init()

    # Tải trước tài nguyên hình ảnh và font chữ
    assets.load_assets()

    # Khởi tạo các scene với màn hình ảo (virtual surface 800x600)
    virtual_screen = display_manager.virtual_surface
    main_menu = MainMenu(virtual_screen, clock)
    difficulty_menu = DifficultyMenu(virtual_screen, clock)
    game_scene = GameScene(virtual_screen, clock)
    game_over_scene = GameOverScene(virtual_screen, clock)

    # State Machine
    state = "MAIN_MENU"
    current_difficulty = "EASY"
    current_speed = DIFFICULTY_SPEEDS["EASY"]
    last_score = 0
    is_new_record = False

    while state != "QUIT":
        if state == "MAIN_MENU":
            action = main_menu.run()
            if action == "START":
                state = "DIFFICULTY_MENU"
            else:
                state = "QUIT"

        elif state == "DIFFICULTY_MENU":
            result = difficulty_menu.run()
            if result == "QUIT":
                state = "QUIT"
            elif result == "BACK":
                state = "MAIN_MENU"
            else:
                current_difficulty, current_speed = result
                state = "PLAYING"

        elif state == "PLAYING":
            status, score, is_new_record = game_scene.run(current_speed, current_difficulty)
            last_score = score
            if status == "GAMEOVER":
                state = "GAME_OVER"
            else:
                state = "QUIT"

        elif state == "GAME_OVER":
            action = game_over_scene.run(last_score, current_difficulty, is_new_record)
            if action == "RESTART":
                state = "PLAYING"
            elif action == "MENU":
                state = "MAIN_MENU"
            else:
                state = "QUIT"

    sound_manager.stop_bgm()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
