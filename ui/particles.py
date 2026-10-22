import random
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GOLD, CYAN, WHITE

class AmbientParticles:
    """Các hạt bụi sáng trôi nhẹ nhàng trong nền menu giúp màn hình sống động."""
    def __init__(self, count=35):
        self.particles = []
        for _ in range(count):
            self.particles.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "radius": random.uniform(1.2, 2.8),
                "speed_y": random.uniform(0.3, 1.2),
                "alpha": random.randint(50, 160),
                "color": random.choice([CYAN, GOLD, (200, 220, 255)])
            })

    def update_and_draw(self, screen):
        for p in self.particles:
            p["y"] += p["speed_y"]
            if p["y"] > SCREEN_HEIGHT:
                p["y"] = -10
                p["x"] = random.randint(0, SCREEN_WIDTH)

            # Vẽ hạt có độ mờ alpha
            surf = pygame.Surface((int(p["radius"] * 2) + 2, int(p["radius"] * 2) + 2), pygame.SRCALPHA)
            color_with_alpha = (*p["color"], p["alpha"])
            pygame.draw.circle(surf, color_with_alpha, (int(p["radius"]) + 1, int(p["radius"]) + 1), int(p["radius"]))
            screen.blit(surf, (int(p["x"]), int(p["y"])))


class CelebrationSparks:
    """Hiệu ứng pháo hoa tia sáng chúc mừng khi phá kỷ lục mới."""
    def __init__(self):
        self.sparks = []

    def burst(self, center_x, center_y, count=50):
        for _ in range(count):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2.0, 7.0)
            self.sparks.append({
                "x": float(center_x),
                "y": float(center_y),
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(30, 60),
                "color": random.choice([GOLD, (255, 230, 100), WHITE, CYAN])
            })

    def update_and_draw(self, screen):
        alive_sparks = []
        for s in self.sparks:
            s["x"] += s["vx"]
            s["y"] += s["vy"]
            s["vy"] += 0.12  # Trọng lực nhẹ
            s["life"] -= 1

            if s["life"] > 0:
                alpha = int(255 * (s["life"] / 60))
                surf = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*s["color"], alpha), (3, 3), 2)
                screen.blit(surf, (int(s["x"]), int(s["y"])))
                alive_sparks.append(s)

        self.sparks = alive_sparks

import math
