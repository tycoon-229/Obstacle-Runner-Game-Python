import pygame
from config import SCREEN_HEIGHT

class ScrollingBackground:
    """
    Quản lý nền cuộn dọc liên tục (Vertical Scrolling Background).
    Sử dụng 2 bản sao hình nền trượt nối tiếp nhau để tạo cảm giác chuyển động mượt mà.
    """
    def __init__(self, image, base_speed=3.0):
        self.image = image
        self.height = SCREEN_HEIGHT
        self.y1 = 0.0
        self.y2 = float(-self.height)
        self.base_speed = base_speed

    def update(self, speed=None):
        scroll_speed = speed if speed is not None else self.base_speed
        self.y1 += scroll_speed
        self.y2 += scroll_speed

        # Khi tấm nền 1 trôi ra khỏi đáy màn hình thì dời lên phía trên tấm nền 2
        if self.y1 >= self.height:
            self.y1 = self.y2 - self.height

        # Khi tấm nền 2 trôi ra khỏi đáy màn hình thì dời lên phía trên tấm nền 1
        if self.y2 >= self.height:
            self.y2 = self.y1 - self.height

    def draw(self, screen):
        screen.blit(self.image, (0, int(self.y1)))
        screen.blit(self.image, (0, int(self.y2)))
