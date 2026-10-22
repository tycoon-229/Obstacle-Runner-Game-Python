import pygame
from config import WHITE, UI_CARD_BG, UI_CARD_BORDER, UI_TEXT_MUTED
from assets import assets

class UIButton:
    """
    Nút bấm giao diện hiện đại hỗ trợ tương tác chuột và phím tắt bàn phím.
    Có hiệu ứng hover mượt mà, viền phát quang và phím tắt trực quan.
    """
    def __init__(
        self,
        rect,
        text,
        shortcut_text=None,
        shortcut_key=None,
        accent_color=(0, 220, 255),
        subtext=None,
        font=None
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.shortcut_text = shortcut_text
        self.shortcut_key = shortcut_key
        self.accent_color = accent_color
        self.subtext = subtext

        self.font = font or assets.button_font
        self.is_hovered = False
        self.hover_progress = 0.0  # 0.0 -> 1.0 animation

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        target = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target - self.hover_progress) * 0.25

    def is_clicked(self, event):
        """Kiểm tra xem nút có được click chuột hoặc kích hoạt bằng phím tắt không."""
        from utils.sound_manager import sound_manager
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                sound_manager.play("click")
                return True

        if event.type == pygame.KEYDOWN and self.shortcut_key is not None:
            if event.key == self.shortcut_key:
                sound_manager.play("click")
                return True

        return False

    def draw(self, screen):
        # Hiệu ứng nhấc nhẹ nút lên 2px khi hover
        offset_y = int(self.hover_progress * -2)
        draw_rect = self.rect.move(0, offset_y)

        # Màu nền nội suy theo hover
        bg_r = int(UI_CARD_BG[0] + self.hover_progress * 15)
        bg_g = int(UI_CARD_BG[1] + self.hover_progress * 20)
        bg_b = int(UI_CARD_BG[2] + self.hover_progress * 30)
        bg_color = (bg_r, bg_g, bg_b, 235)

        # Màu viền phát sáng khi hover
        border_r = int(UI_CARD_BORDER[0] + self.hover_progress * (self.accent_color[0] - UI_CARD_BORDER[0]))
        border_g = int(UI_CARD_BORDER[1] + self.hover_progress * (self.accent_color[1] - UI_CARD_BORDER[1]))
        border_b = int(UI_CARD_BORDER[2] + self.hover_progress * (self.accent_color[2] - UI_CARD_BORDER[2]))
        border_color = (border_r, border_g, border_b)

        # Vẽ nền kính mờ
        panel = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, bg_color, (0, 0, draw_rect.width, draw_rect.height), border_radius=12)

        # Vẽ dải nhấn màu mỏng ở mép trái khi hover
        if self.hover_progress > 0.05:
            accent_alpha = int(self.hover_progress * 255)
            accent_bar = pygame.Surface((5, draw_rect.height - 8), pygame.SRCALPHA)
            accent_bar.fill((*self.accent_color, accent_alpha))
            panel.blit(accent_bar, (4, 4))

        # Viền nút
        border_width = 2 if self.hover_progress > 0.2 else 1
        pygame.draw.rect(panel, border_color, (0, 0, draw_rect.width, draw_rect.height), width=border_width, border_radius=12)
        screen.blit(panel, (draw_rect.x, draw_rect.y))

        # Vẽ text chính
        text_color = WHITE if not self.is_hovered else (255, 255, 255)
        rendered_text = self.font.render(self.text, True, text_color)

        if self.subtext:
            # Nếu có dòng mô tả nhỏ bên dưới
            text_y = draw_rect.y + (draw_rect.height // 2) - 14
            screen.blit(rendered_text, (draw_rect.x + 22, text_y))

            sub_surf = assets.badge_font.render(self.subtext, True, UI_TEXT_MUTED)
            screen.blit(sub_surf, (draw_rect.x + 22, text_y + 24))
        else:
            text_rect = rendered_text.get_rect(midleft=(draw_rect.x + 22, draw_rect.centery))
            screen.blit(rendered_text, text_rect)

        # Vẽ phím tắt [ KEY ] ở bên phải nút nếu có
        if self.shortcut_text:
            badge_surf = assets.badge_font.render(f"[{self.shortcut_text}]", True, border_color)
            badge_rect = badge_surf.get_rect(midright=(draw_rect.right - 18, draw_rect.centery))
            screen.blit(badge_surf, badge_rect)
