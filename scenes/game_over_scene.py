import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    GOLD,
    UI_ACCENT_RED,
    UI_ACCENT_GREEN,
    UI_ACCENT_CYAN,
    UI_TEXT_MUTED
)
from assets import assets
from utils import score_manager, sound_manager, display_manager
from ui import draw_glass_panel, UIButton, AmbientParticles, CelebrationSparks

class GameOverScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.particles = AmbientParticles(20)
        self.sparks = CelebrationSparks()

    def run(self, score, difficulty="EASY", is_new_record=False):
        """Màn hình kết thúc trận đấu hỗ trợ co giãn màn hình và âm thanh."""
        high_score = score_manager.get_high_score(difficulty)

        card_w = 480
        card_h = 500
        card_x = (SCREEN_WIDTH - card_w) // 2
        card_y = 50

        # Nếu phá kỷ lục thì bung pháo hoa tia sáng
        if is_new_record:
            self.sparks.burst(SCREEN_WIDTH // 2, card_y + 100, count=70)

        btn_restart = UIButton(
            rect=(card_x + 35, card_y + 280, 410, 56),
            text="PLAY AGAIN",
            shortcut_text="R",
            shortcut_key=pygame.K_r,
            accent_color=UI_ACCENT_GREEN,
            subtext="Restart immediately with current difficulty"
        )
        btn_menu = UIButton(
            rect=(card_x + 35, card_y + 350, 410, 52),
            text="MAIN MENU",
            shortcut_text="M",
            shortcut_key=pygame.K_m,
            accent_color=UI_ACCENT_CYAN
        )
        btn_quit = UIButton(
            rect=(card_x + 35, card_y + 415, 410, 48),
            text="QUIT GAME",
            shortcut_text="Q",
            shortcut_key=pygame.K_q,
            accent_color=UI_ACCENT_RED
        )

        buttons = [btn_restart, btn_menu, btn_quit]
        tick = 0

        while True:
            tick += 1
            mouse_pos = display_manager.map_mouse_pos(pygame.mouse.get_pos())
            for btn in buttons:
                btn.update(mouse_pos)

            render_surf = display_manager.virtual_surface
            render_surf.blit(assets.background, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 12, 22, 205))
            render_surf.blit(overlay, (0, 0))

            self.particles.update_and_draw(render_surf)
            if is_new_record:
                self.sparks.update_and_draw(render_surf)

            # Khung thẻ kết quả Glassmorphism
            draw_glass_panel(render_surf, (card_x, card_y, card_w, card_h), border_radius=18)

            # Tiêu đề GAME OVER
            over_shadow = assets.header_font.render("GAME OVER", True, (100, 20, 30))
            over_surf = assets.header_font.render("GAME OVER", True, UI_ACCENT_RED)
            render_surf.blit(over_shadow, (card_x + (card_w - over_surf.get_width()) // 2 + 2, card_y + 24))
            render_surf.blit(over_surf, (card_x + (card_w - over_surf.get_width()) // 2, card_y + 22))

            # Banner thông báo kỷ lục mới nếu có
            if is_new_record:
                rec_pulse = 200 + int(55 * (0.5 + 0.5 * pygame.math.Vector2(1, 0).rotate(tick * 5).x))
                rec_color = (rec_pulse, 200, 20)
                rec_text = assets.button_font.render("★ NEW BEST RECORD! ★", True, rec_color)
                render_surf.blit(rec_text, (card_x + (card_w - rec_text.get_width()) // 2, card_y + 70))
            else:
                mode_badge = assets.badge_font.render(f"Difficulty: {difficulty}", True, UI_TEXT_MUTED)
                render_surf.blit(mode_badge, (card_x + (card_w - mode_badge.get_width()) // 2, card_y + 70))

            # Hai ô so sánh điểm (Score Grid)
            grid_y = card_y + 115
            cell_w = 195
            cell_h = 135

            # Ô 1: Điểm hiện tại
            draw_glass_panel(render_surf, (card_x + 35, grid_y, cell_w, cell_h), fill_color=(25, 33, 52, 240), border_radius=12)
            lbl_score = assets.badge_font.render("YOUR SCORE", True, UI_TEXT_MUTED)
            val_score = assets.title_font.render(str(score), True, WHITE)
            render_surf.blit(lbl_score, (card_x + 35 + (cell_w - lbl_score.get_width()) // 2, grid_y + 20))
            render_surf.blit(val_score, (card_x + 35 + (cell_w - val_score.get_width()) // 2, grid_y + 50))

            # Ô 2: Kỷ lục cao nhất
            draw_glass_panel(render_surf, (card_x + 250, grid_y, cell_w, cell_h), fill_color=(25, 33, 52, 240), border_radius=12)
            lbl_best = assets.badge_font.render("BEST RECORD", True, GOLD)
            val_best = assets.title_font.render(str(high_score), True, GOLD)
            render_surf.blit(lbl_best, (card_x + 250 + (cell_w - lbl_best.get_width()) // 2, grid_y + 20))
            render_surf.blit(val_best, (card_x + 250 + (cell_w - val_best.get_width()) // 2, grid_y + 50))

            # Vẽ các nút thao tác
            for btn in buttons:
                btn.draw(render_surf)

            display_manager.present()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                display_manager.handle_event(event)

                if btn_restart.is_clicked(event):
                    return "RESTART"

                if btn_menu.is_clicked(event):
                    return "MENU"

                if btn_quit.is_clicked(event):
                    return "QUIT"

            self.clock.tick(60)
