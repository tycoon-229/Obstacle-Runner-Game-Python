import pygame
from config import UI_CARD_BG, UI_CARD_BORDER, WHITE

def draw_glass_panel(surface, rect, fill_color=UI_CARD_BG, border_color=UI_CARD_BORDER, border_radius=14, border_width=2):
    """
    Vẽ bảng hiệu ứng kính mờ (Glassmorphism card).
    Sử dụng Surface trong suốt có bo góc mềm mại và viền phản quang hiện đại.
    """
    if isinstance(rect, tuple):
        rect = pygame.Rect(rect)

    # Lớp nền bán trong suốt
    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(panel, fill_color, (0, 0, rect.width, rect.height), border_radius=border_radius)

    # Viền kính phản quang
    if border_color and border_width > 0:
        pygame.draw.rect(panel, border_color, (0, 0, rect.width, rect.height), width=border_width, border_radius=border_radius)

    surface.blit(panel, (rect.x, rect.y))

def draw_pill_badge(surface, x, y, text, font, bg_color=(25, 35, 55, 220), text_color=WHITE, border_color=None, padding_x=12, padding_y=4):
    """
    Vẽ nhãn dạng viên thuốc (Pill Badge) bo tròn hiện đại cho HUD hoặc trạng thái.
    """
    rendered_text = font.render(text, True, text_color)
    width = rendered_text.get_width() + padding_x * 2
    height = rendered_text.get_height() + padding_y * 2

    badge_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    radius = height // 2
    pygame.draw.rect(badge_surf, bg_color, (0, 0, width, height), border_radius=radius)

    if border_color:
        pygame.draw.rect(badge_surf, border_color, (0, 0, width, height), width=1, border_radius=radius)

    badge_surf.blit(rendered_text, (padding_x, padding_y))
    surface.blit(badge_surf, (x, y))
    return width, height
