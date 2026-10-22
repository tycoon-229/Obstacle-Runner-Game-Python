"""
Quản lý độ phân giải màn hình, tỉ lệ co giãn (Scaling) và Toàn màn hình (Fullscreen).
Sử dụng kỹ thuật Virtual Surface (Canvas ảo 800x600):
- Cho phép phóng to lên 1200x900, 1600x1200, 1920x1080 hoặc Fullscreen.
- Giữ vững tỉ lệ chuẩn, không làm méo hình.
- Tự động chuyển đổi tọa độ chuột (Mouse Coordinate Remapping).
"""
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class DisplayManager:
    _instance = None

    RESOLUTIONS = [
        {"name": "800 x 600 (Standard)", "width": 800, "height": 600},
        {"name": "1200 x 900 (Large 1.5x)", "width": 1200, "height": 900},
        {"name": "1600 x 1200 (HD 2.0x)", "width": 1600, "height": 1200},
        {"name": "1920 x 1080 (Full HD 16:9)", "width": 1920, "height": 1080},
    ]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DisplayManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def init(self):
        if self.initialized:
            return

        self.virtual_width = SCREEN_WIDTH
        self.virtual_height = SCREEN_HEIGHT
        self.virtual_surface = pygame.Surface((self.virtual_width, self.virtual_height))

        self.window_width = SCREEN_WIDTH
        self.window_height = SCREEN_HEIGHT
        self.is_fullscreen = False
        self.current_res_index = 0

        # Khởi tạo cửa sổ hỗ trợ co giãn tự do (RESIZABLE)
        self.window = pygame.display.set_mode(
            (self.window_width, self.window_height),
            pygame.RESIZABLE
        )
        pygame.display.set_caption("Obstacle Runner")

        self._recompute_viewport()
        self.initialized = True

    def _recompute_viewport(self):
        """Tính toán kích thước và vị trí căn giữa khung hình ảo trong cửa sổ thực tế."""
        scale_x = self.window_width / self.virtual_width
        scale_y = self.window_height / self.virtual_height
        scale = min(scale_x, scale_y)

        self.scaled_width = int(self.virtual_width * scale)
        self.scaled_height = int(self.virtual_height * scale)

        self.offset_x = (self.window_width - self.scaled_width) // 2
        self.offset_y = (self.window_height - self.scaled_height) // 2
        self.scale = scale

    def handle_event(self, event):
        """Bắt các sự kiện thay đổi kích thước cửa sổ hoặc phím F11 toàn màn hình."""
        if event.type == pygame.VIDEORESIZE:
            self.window_width = max(640, event.w)
            self.window_height = max(480, event.h)
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
            self._recompute_viewport()
            return True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            self.toggle_fullscreen()
            return True

        return False

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Lấy độ phân giải màn hình desktop thực tế
            info = pygame.display.Info()
            self.window_width = info.current_w
            self.window_height = info.current_h
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.FULLSCREEN | pygame.RESIZABLE
            )
        else:
            res = self.RESOLUTIONS[self.current_res_index]
            self.window_width = res["width"]
            self.window_height = res["height"]
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
        self._recompute_viewport()

    def set_resolution_index(self, index):
        if 0 <= index < len(self.RESOLUTIONS):
            self.current_res_index = index
            res = self.RESOLUTIONS[index]
            self.window_width = res["width"]
            self.window_height = res["height"]
            self.is_fullscreen = False
            self.window = pygame.display.set_mode(
                (self.window_width, self.window_height),
                pygame.RESIZABLE
            )
            self._recompute_viewport()

    def cycle_resolution(self):
        """Chuyển đổi tuần hoàn qua các độ phân giải có sẵn."""
        next_idx = (self.current_res_index + 1) % len(self.RESOLUTIONS)
        self.set_resolution_index(next_idx)
        return self.RESOLUTIONS[next_idx]["name"]

    def map_mouse_pos(self, window_mouse_pos):
        """Chuyển đổi tọa độ chuột từ cửa sổ thực về tọa độ của màn hình ảo 800x600."""
        mx, my = window_mouse_pos
        vx = (mx - self.offset_x) / self.scale if self.scale > 0 else 0
        vy = (my - self.offset_y) / self.scale if self.scale > 0 else 0
        return int(vx), int(vy)

    def present(self):
        """Vẽ khung hình ảo 800x600 đã co giãn lên cửa sổ thực tế và làm mới màn hình."""
        # Xóa viền đen bằng màu nền tối
        self.window.fill((6, 8, 14))

        # Co giãn bề mặt ảo
        if self.scaled_width == self.virtual_width and self.scaled_height == self.virtual_height:
            scaled_surf = self.virtual_surface
        else:
            scaled_surf = pygame.transform.smoothscale(
                self.virtual_surface,
                (self.scaled_width, self.scaled_height)
            )

        self.window.blit(scaled_surf, (self.offset_x, self.offset_y))
        pygame.display.flip()

display_manager = DisplayManager()
