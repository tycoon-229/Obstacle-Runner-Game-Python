import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, UI_ACCENT_CYAN, UI_ACCENT_GOLD, UI_ACCENT_GREEN, UI_ACCENT_RED, UI_TEXT_MUTED
from assets import assets
from utils import sound_manager, display_manager
from ui import draw_glass_panel, UIButton

class PauseScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

    def run(self):
        """Màn hình tạm dừng với cửa sổ Modal hỗ trợ chỉnh âm thanh và độ phân giải."""
        modal_w = 420
        modal_h = 350
        modal_x = (SCREEN_WIDTH - modal_w) // 2
        modal_y = (SCREEN_HEIGHT - modal_h) // 2

        btn_continue = UIButton(
            rect=(modal_x + 30, modal_y + 90, 360, 50),
            text="RESUME GAME",
            shortcut_text="P",
            shortcut_key=pygame.K_p,
            accent_color=UI_ACCENT_CYAN
        )
        btn_res = UIButton(
            rect=(modal_x + 30, modal_y + 150, 360, 46),
            text="DISPLAY: SCALE",
            shortcut_text="TAB / F11",
            shortcut_key=pygame.K_TAB,
            accent_color=UI_ACCENT_GOLD
        )
        btn_sound = UIButton(
            rect=(modal_x + 30, modal_y + 206, 360, 46),
            text="SOUND: ON",
            shortcut_text="M",
            shortcut_key=pygame.K_m,
            accent_color=UI_ACCENT_GREEN
        )
        btn_quit = UIButton(
            rect=(modal_x + 30, modal_y + 262, 360, 46),
            text="QUIT TO MENU",
            shortcut_text="Q",
            shortcut_key=pygame.K_q,
            accent_color=UI_ACCENT_RED
        )

        buttons = [btn_continue, btn_res, btn_sound, btn_quit]

        # Chụp lại khung hình game trên màn hình ảo
        captured_bg = display_manager.virtual_surface.copy()
        dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        dim_overlay.fill((6, 10, 18, 185))

        while True:
            mouse_pos = display_manager.map_mouse_pos(pygame.mouse.get_pos())
            for btn in buttons:
                btn.update(mouse_pos)

            # Cập nhật text trạng thái
            res_name = display_manager.RESOLUTIONS[display_manager.current_res_index]["name"]
            btn_res.text = "MODE: FULLSCREEN" if display_manager.is_fullscreen else f"SCALE: {res_name.split(' (')[0]}"
            btn_sound.text = "SOUND: MUTED" if sound_manager.muted else "SOUND: ON"
            btn_sound.accent_color = UI_ACCENT_RED if sound_manager.muted else UI_ACCENT_GREEN

            render_surf = display_manager.virtual_surface
            render_surf.blit(captured_bg, (0, 0))
            render_surf.blit(dim_overlay, (0, 0))

            # Modal Dialog
            draw_glass_panel(render_surf, (modal_x, modal_y, modal_w, modal_h), border_radius=16)

            title_surf = assets.header_font.render("GAME PAUSED", True, WHITE)
            render_surf.blit(title_surf, (modal_x + (modal_w - title_surf.get_width()) // 2, modal_y + 24))

            sub_surf = assets.badge_font.render("Press P to continue or adjust settings", True, UI_TEXT_MUTED)
            render_surf.blit(sub_surf, (modal_x + (modal_w - sub_surf.get_width()) // 2, modal_y + 60))

            for btn in buttons:
                btn.draw(render_surf)

            display_manager.present()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"

                display_manager.handle_event(event)

                if btn_continue.is_clicked(event):
                    return "CONTINUE"

                if btn_res.is_clicked(event):
                    display_manager.cycle_resolution()

                if btn_sound.is_clicked(event):
                    sound_manager.toggle_mute()

                if btn_quit.is_clicked(event):
                    return "QUIT"

            self.clock.tick(30)
