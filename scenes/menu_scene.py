import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GOLD,
    UI_CARD_BORDER,
    UI_TEXT_MUTED,
    UI_ACCENT_CYAN,
    UI_ACCENT_GREEN,
    UI_ACCENT_GOLD,
    UI_ACCENT_RED,
    DIFFICULTY_SPEEDS
)
from assets import assets
from utils import score_manager, sound_manager, display_manager
from ui import draw_glass_panel, draw_pill_badge, UIButton, AmbientParticles

class MainMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.particles = AmbientParticles(30)

        card_x = (SCREEN_WIDTH - 440) // 2
        card_y = 75

        self.btn_start = UIButton(
            rect=(card_x + 30, card_y + 155, 380, 54),
            text="START MISSION",
            shortcut_text="SPACE",
            shortcut_key=pygame.K_SPACE,
            accent_color=UI_ACCENT_CYAN,
            subtext="Choose difficulty and start running"
        )
        self.btn_res = UIButton(
            rect=(card_x + 30, card_y + 220, 380, 48),
            text="SCALE: 800 x 600",
            shortcut_text="F11 / TAB",
            shortcut_key=pygame.K_TAB,
            accent_color=UI_ACCENT_GOLD,
            subtext="Click or TAB to cycle resolution, F11 Fullscreen"
        )
        self.btn_sound = UIButton(
            rect=(card_x + 30, card_y + 278, 380, 48),
            text="SOUND: ON",
            shortcut_text="M",
            shortcut_key=pygame.K_m,
            accent_color=UI_ACCENT_GREEN,
            subtext="Toggle SFX and Background Music"
        )
        self.btn_quit = UIButton(
            rect=(card_x + 30, card_y + 336, 380, 46),
            text="QUIT GAME",
            shortcut_text="Q",
            shortcut_key=pygame.K_q,
            accent_color=UI_ACCENT_RED
        )

        self.buttons = [self.btn_start, self.btn_res, self.btn_sound, self.btn_quit]

    def run(self):
        """Chạy màn hình menu chính với hỗ trợ đổi kích thước màn hình và âm thanh."""
        card_w = 440
        card_h = 445
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = 75

        while True:
            # Chuyển đổi tọa độ chuột từ cửa sổ thực tế sang màn hình ảo 800x600
            mouse_pos = display_manager.map_mouse_pos(pygame.mouse.get_pos())
            for btn in self.buttons:
                btn.update(mouse_pos)

            # Cập nhật nhãn nút cài đặt
            res_name = display_manager.RESOLUTIONS[display_manager.current_res_index]["name"]
            if display_manager.is_fullscreen:
                self.btn_res.text = "MODE: FULLSCREEN (F11)"
            else:
                self.btn_res.text = f"SCALE: {res_name.split(' (')[0]}"

            self.btn_sound.text = "SOUND: MUTED" if sound_manager.muted else "SOUND: ON"
            self.btn_sound.accent_color = UI_ACCENT_RED if sound_manager.muted else UI_ACCENT_GREEN

            # Render lên Virtual Canvas
            render_surf = display_manager.virtual_surface
            render_surf.blit(assets.background, (0, 0))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 12, 22, 185))
            render_surf.blit(overlay, (0, 0))

            self.particles.update_and_draw(render_surf)

            # Card trung tâm Glassmorphism
            draw_glass_panel(render_surf, (card_x, card_y, card_w, card_h), border_radius=18)

            # Tiêu đề game hiện đại
            title_shadow = assets.title_font.render("OBSTACLE RUNNER", True, (0, 110, 150))
            title_surf = assets.title_font.render("OBSTACLE RUNNER", True, WHITE)
            render_surf.blit(title_shadow, (card_x + (card_w - title_surf.get_width()) // 2 + 2, card_y + 24))
            render_surf.blit(title_surf, (card_x + (card_w - title_surf.get_width()) // 2, card_y + 22))

            # Đường neon trang trí
            line_w = 260
            line_x = card_x + (card_w - line_w) // 2
            pygame.draw.line(render_surf, UI_ACCENT_CYAN, (line_x, card_y + 82), (line_x + line_w, card_y + 82), 2)

            # Badge kỷ lục
            all_time_high = score_manager.get_high_score("ALL_TIME_BEST")
            draw_pill_badge(
                render_surf,
                x=card_x + (card_w - 200) // 2,
                y=card_y + 98,
                text=f"BEST SCORE: {all_time_high}",
                font=assets.badge_font,
                bg_color=(35, 45, 25, 230),
                text_color=GOLD,
                border_color=(120, 100, 20)
            )

            # Vẽ các nút
            for btn in self.buttons:
                btn.draw(render_surf)

            # Hướng dẫn điều khiển nhỏ ở chân card
            hints_text = "Free Move: W A S D / Arrow Keys   •   F11: Fullscreen"
            hint_surf = assets.badge_font.render(hints_text, True, UI_TEXT_MUTED)
            render_surf.blit(hint_surf, (card_x + (card_w - hint_surf.get_width()) // 2, card_y + card_h - 26))

            # Co giãn và trình chiếu lên màn hình thực tế
            display_manager.present()

            # Bắt sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                display_manager.handle_event(event)

                if self.btn_start.is_clicked(event):
                    return "START"

                if self.btn_res.is_clicked(event):
                    display_manager.cycle_resolution()

                if self.btn_sound.is_clicked(event):
                    sound_manager.toggle_mute()

                if self.btn_quit.is_clicked(event):
                    return "QUIT"

            self.clock.tick(60)


class DifficultyMenu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.particles = AmbientParticles(25)

    def run(self):
        """Màn hình chọn độ khó phong cách thẻ bài hiện đại."""
        card_w = 480
        card_h = 470
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = 65

        btn_easy = UIButton(
            rect=(card_x + 30, card_y + 110, 420, 68),
            text="EASY MODE",
            shortcut_text="1",
            shortcut_key=pygame.K_1,
            accent_color=UI_ACCENT_GREEN,
            subtext=f"Slower obstacles  •  Record: {score_manager.get_high_score('EASY')}"
        )
        btn_medium = UIButton(
            rect=(card_x + 30, card_y + 190, 420, 68),
            text="MEDIUM MODE",
            shortcut_text="2",
            shortcut_key=pygame.K_2,
            accent_color=UI_ACCENT_GOLD,
            subtext=f"Balanced speed  •  Record: {score_manager.get_high_score('MEDIUM')}"
        )
        btn_hard = UIButton(
            rect=(card_x + 30, card_y + 270, 420, 68),
            text="HARD MODE",
            shortcut_text="3",
            shortcut_key=pygame.K_3,
            accent_color=UI_ACCENT_RED,
            subtext=f"Extreme speed & danger  •  Record: {score_manager.get_high_score('HARD')}"
        )
        btn_back = UIButton(
            rect=(card_x + 30, card_y + 365, 420, 48),
            text="BACK TO MENU",
            shortcut_text="ESC",
            shortcut_key=pygame.K_ESCAPE,
            accent_color=UI_TEXT_MUTED
        )

        buttons = [btn_easy, btn_medium, btn_hard, btn_back]

        while True:
            mouse_pos = display_manager.map_mouse_pos(pygame.mouse.get_pos())
            for btn in buttons:
                btn.update(mouse_pos)

            render_surf = display_manager.virtual_surface
            render_surf.blit(assets.background, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 12, 22, 190))
            render_surf.blit(overlay, (0, 0))
            self.particles.update_and_draw(render_surf)

            draw_glass_panel(render_surf, (card_x, card_y, card_w, card_h), border_radius=18)

            header_surf = assets.header_font.render("SELECT DIFFICULTY", True, WHITE)
            render_surf.blit(header_surf, (card_x + (card_w - header_surf.get_width()) // 2, card_y + 28))

            sub_header = assets.badge_font.render("Choose your initial game challenge level", True, UI_TEXT_MUTED)
            render_surf.blit(sub_header, (card_x + (card_w - sub_header.get_width()) // 2, card_y + 70))

            for btn in buttons:
                btn.draw(render_surf)

            display_manager.present()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                display_manager.handle_event(event)

                if btn_easy.is_clicked(event):
                    return "EASY", DIFFICULTY_SPEEDS["EASY"]

                if btn_medium.is_clicked(event):
                    return "MEDIUM", DIFFICULTY_SPEEDS["MEDIUM"]

                if btn_hard.is_clicked(event):
                    return "HARD", DIFFICULTY_SPEEDS["HARD"]

                if btn_back.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_q)):
                    return "BACK"

            self.clock.tick(60)
