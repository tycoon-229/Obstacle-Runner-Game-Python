import pygame
import random
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WHITE,
    CYAN,
    GOLD,
    PLAYER_START_X,
    PLAYER_START_Y,
    PLAYER_MAX_HP,
    OBSTACLE_COUNT,
    SPEED_INCREMENT_SCORE_INTERVAL,
    SPEED_INCREMENT_AMOUNT,
    POWERUP_SPAWN_CHANCE,
    POWERUP_SCORE_BONUS,
    SLOW_MO_DURATION,
    SLOW_MO_FACTOR,
    BACKGROUND_SCROLL_SPEED,
    METEOR_SPAWN_INTERVAL,
    UI_CARD_BORDER,
    UI_TEXT_MUTED,
    UI_ACCENT_CYAN,
    UI_ACCENT_GOLD,
    UI_ACCENT_GREEN,
    UI_ACCENT_RED
)
from assets import assets
from entities import Player, Obstacle, FastMeteor, PowerUp, ScrollingBackground
from utils import score_manager, sound_manager, display_manager
from ui import draw_glass_panel, draw_pill_badge
from .pause_scene import PauseScene

class FloatingText:
    """Các dòng chữ thông báo bay lên và mờ dần khi nhặt đồ hoặc mất máu."""
    def __init__(self, x, y, text, color):
        self.x = float(x)
        self.y = float(y)
        self.text = text
        self.color = color
        self.alpha = 255
        self.life = 45

    def update(self):
        self.y -= 1.2
        self.life -= 1
        self.alpha = max(0, int(255 * (self.life / 45)))
        return self.life > 0

    def draw(self, screen):
        text_surf = assets.badge_font.render(self.text, True, self.color)
        surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        surf.blit(text_surf, (0, 0))
        surf.set_alpha(self.alpha)
        screen.blit(surf, (int(self.x), int(self.y)))


class GameScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.pause_scene = PauseScene(screen, clock)

    def run(self, initial_speed, difficulty_name="EASY"):
        """
        Vòng lặp chơi game chính với:
        - Di chuyển tự do 4 hướng (W, A, S, D / Mũi tên).
        - Âm thanh SFX & BGM sống động.
        - Co giãn màn hình ảo (Virtual Canvas Scaler) tương thích mọi kích thước màn hình.
        """
        sound_manager.start_bgm()
        scrolling_bg = ScrollingBackground(assets.background, base_speed=BACKGROUND_SCROLL_SPEED)

        all_sprites = pygame.sprite.Group()
        obstacles_group = pygame.sprite.Group()
        meteors_group = pygame.sprite.Group()
        powerups_group = pygame.sprite.Group()

        player = Player(PLAYER_START_X, PLAYER_START_Y, assets.player_img)
        all_sprites.add(player)

        current_speed = float(initial_speed)
        for i in range(OBSTACLE_COUNT):
            is_wavy = (i % 2 == 1)
            obs = Obstacle(assets.obstacle_img, current_speed, is_wavy=is_wavy)
            all_sprites.add(obs)
            obstacles_group.add(obs)

        score = 0
        slow_mo_timer = 0
        meteor_timer = random.randint(*METEOR_SPAWN_INTERVAL)
        best_record = score_manager.get_high_score(difficulty_name)
        floating_texts = []
        screen_shake = 0
        running = True

        while running:
            # 1. Hệ số tốc độ & Slow-Motion
            if slow_mo_timer > 0:
                slow_mo_timer -= 1
                effective_speed = current_speed * SLOW_MO_FACTOR
            else:
                effective_speed = current_speed

            # 2. Xử lý Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sound_manager.stop_bgm()
                    is_new_rec = score_manager.update_high_score(score, difficulty_name)
                    return "QUIT", score, is_new_rec

                # Bắt sự kiện co giãn cửa sổ / F11 Fullscreen
                display_manager.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    # Di chuyển ngang
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        player.speed_x = -player.move_speed
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        player.speed_x = player.move_speed

                    # Di chuyển dọc (Lên / Xuống tự do)
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        player.speed_y = -player.move_speed
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        player.speed_y = player.move_speed

                    # Bật/tắt âm thanh nhanh bằng phím M
                    elif event.key == pygame.K_m:
                        muted = sound_manager.toggle_mute()
                        msg = "SOUND OFF" if muted else "SOUND ON"
                        floating_texts.append(FloatingText(player.rect.centerx - 30, player.rect.top - 20, msg, UI_ACCENT_GOLD))

                    elif event.key == pygame.K_p:
                        pause_result = self.pause_scene.run()
                        if pause_result == "QUIT":
                            sound_manager.stop_bgm()
                            is_new_rec = score_manager.update_high_score(score, difficulty_name)
                            return "QUIT", score, is_new_rec

                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                        player.speed_x = 0
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                        player.speed_y = 0

            # 3. Sinh vật phẩm
            if random.randint(1, POWERUP_SPAWN_CHANCE) == 1:
                powerup = PowerUp()
                all_sprites.add(powerup)
                powerups_group.add(powerup)

            # 4. Sinh Thiên thạch rơi nhanh
            meteor_timer -= 1
            if meteor_timer <= 0:
                meteor = FastMeteor(effective_speed)
                all_sprites.add(meteor)
                obstacles_group.add(meteor)
                meteors_group.add(meteor)
                meteor_timer = random.randint(*METEOR_SPAWN_INTERVAL)
                sound_manager.play("warning")

            # 5. Cập nhật đối tượng
            scrolling_bg.update(effective_speed * 0.4)
            player.update()
            powerups_group.update()

            for obs in list(obstacles_group):
                if isinstance(obs, FastMeteor):
                    passed = obs.update(effective_speed)
                else:
                    obs.speed_y = effective_speed
                    passed = obs.update()

                if passed:
                    score += 1
                    if score > 0 and score % SPEED_INCREMENT_SCORE_INTERVAL == 0:
                        current_speed += SPEED_INCREMENT_AMOUNT
                        floating_texts.append(FloatingText(SCREEN_WIDTH // 2 - 40, 90, "SPEED UP!", UI_ACCENT_GOLD))

            # 6. Va chạm Pixel-Perfect
            hits = pygame.sprite.spritecollide(player, obstacles_group, False, pygame.sprite.collide_mask)
            if hits:
                damage_result = player.take_damage()
                if damage_result == "SHIELD_BROKEN":
                    sound_manager.play("shield_break")
                    screen_shake = 6
                    floating_texts.append(FloatingText(player.rect.centerx - 45, player.rect.top - 20, "SHIELD BROKEN!", UI_ACCENT_RED))
                elif damage_result == "DAMAGED":
                    sound_manager.play("hit")
                    screen_shake = 12
                    floating_texts.append(FloatingText(player.rect.centerx - 20, player.rect.top - 20, "-1 HP", UI_ACCENT_RED))
                    if player.hp <= 0:
                        sound_manager.stop_bgm()
                        sound_manager.play("game_over")
                        is_new_rec = score_manager.update_high_score(score, difficulty_name)
                        return "GAMEOVER", score, is_new_rec

            # Va chạm nhặt vật phẩm
            power_hits = pygame.sprite.spritecollide(player, powerups_group, True, pygame.sprite.collide_mask)
            for power in power_hits:
                score += POWERUP_SCORE_BONUS
                if power.power_type == PowerUp.TYPE_HEAL:
                    sound_manager.play("heal")
                    if player.hp < PLAYER_MAX_HP:
                        player.hp += 1
                        floating_texts.append(FloatingText(player.rect.centerx - 20, player.rect.top - 20, "+1 HP", UI_ACCENT_GREEN))
                    else:
                        floating_texts.append(FloatingText(player.rect.centerx - 25, player.rect.top - 20, "+BONUS PTS", UI_ACCENT_GREEN))
                elif power.power_type == PowerUp.TYPE_SHIELD:
                    sound_manager.play("shield")
                    player.has_shield = True
                    floating_texts.append(FloatingText(player.rect.centerx - 40, player.rect.top - 20, "SHIELD ACTIVE!", UI_ACCENT_CYAN))
                elif power.power_type == PowerUp.TYPE_SLOW_MO:
                    sound_manager.play("slow_mo")
                    slow_mo_timer = SLOW_MO_DURATION
                    floating_texts.append(FloatingText(player.rect.centerx - 40, player.rect.top - 20, "TIME SLOWED!", UI_ACCENT_GOLD))

            # Cập nhật thông báo nổi
            floating_texts = [ft for ft in floating_texts if ft.update()]

            # 7. Render lên Virtual Canvas (Màn hình ảo chuẩn 800x600)
            render_surface = display_manager.virtual_surface
            shake_x, shake_y = 0, 0
            if screen_shake > 0:
                shake_x = random.randint(-screen_shake, screen_shake)
                shake_y = random.randint(-screen_shake, screen_shake)
                screen_shake -= 1

            # Vẽ nền cuộn
            scrolling_bg.draw(render_surface)

            # Cảnh báo thiên thạch
            for meteor in meteors_group:
                meteor.draw_warning(render_surface)
            for meteor in meteors_group:
                meteor.draw_trail(render_surface)

            all_sprites.draw(render_surface)
            player.draw_effects(render_surface)

            for ft in floating_texts:
                ft.draw(render_surface)

            # =========================
            # HUD HIỆN ĐẠI (TOP GLASS BAR)
            # =========================
            # Capsule 1: Thông số Score, Best và Speed (bên trái)
            hud_card_w = 340
            hud_card_h = 46
            hud_card_x = 16 + shake_x
            hud_card_y = 14 + shake_y
            draw_glass_panel(render_surface, (hud_card_x, hud_card_y, hud_card_w, hud_card_h), border_radius=12)

            # Điểm Score
            s_lbl = assets.badge_font.render("SCORE", True, UI_TEXT_MUTED)
            s_val = assets.hud_font.render(str(score), True, WHITE)
            render_surface.blit(s_lbl, (hud_card_x + 14, hud_card_y + 6))
            render_surface.blit(s_val, (hud_card_x + 14, hud_card_y + 22))

            # Vạch ngăn 1
            pygame.draw.line(render_surface, UI_CARD_BORDER, (hud_card_x + 115, hud_card_y + 10), (hud_card_x + 115, hud_card_y + 36), 1)

            # Điểm Best
            b_lbl = assets.badge_font.render("BEST", True, UI_ACCENT_GOLD)
            cur_best = max(best_record, score)
            b_val = assets.hud_font.render(str(cur_best), True, GOLD)
            render_surface.blit(b_lbl, (hud_card_x + 130, hud_card_y + 6))
            render_surface.blit(b_val, (hud_card_x + 130, hud_card_y + 22))

            # Vạch ngăn 2
            pygame.draw.line(render_surface, UI_CARD_BORDER, (hud_card_x + 225, hud_card_y + 10), (hud_card_x + 225, hud_card_y + 36), 1)

            # Tốc độ Speed
            spd_lbl = assets.badge_font.render("SPEED", True, UI_ACCENT_CYAN)
            spd_val = assets.hud_font.render(f"{round(effective_speed, 1)}x", True, CYAN)
            render_surface.blit(spd_lbl, (hud_card_x + 240, hud_card_y + 6))
            render_surface.blit(spd_val, (hud_card_x + 240, hud_card_y + 22))

            # Capsule 2: Khung chứa thanh máu Trái Tim (bên phải)
            hp_card_w = 148
            hp_card_h = 46
            hp_card_x = SCREEN_WIDTH - hp_card_w - 16 + shake_x
            hp_card_y = 14 + shake_y
            draw_glass_panel(render_surface, (hp_card_x, hp_card_y, hp_card_w, hp_card_h), border_radius=12)

            for i in range(player.hp):
                hx = hp_card_x + 16 + (i * 42)
                hy = hp_card_y + 7
                render_surface.blit(assets.heart_img, (hx, hy))

            # Badge trạng thái Khiên chắn
            if player.has_shield:
                draw_pill_badge(
                    render_surface,
                    x=hp_card_x,
                    y=hp_card_y + 54,
                    text="SHIELD ACTIVE",
                    font=assets.badge_font,
                    bg_color=(15, 40, 55, 230),
                    text_color=CYAN,
                    border_color=UI_ACCENT_CYAN
                )

            # Badge trạng thái Slow-Mo
            if slow_mo_timer > 0:
                slow_time_sec = round(slow_mo_timer / FPS, 1)
                slow_text = f"SLOW-MO  {slow_time_sec}s"
                badge_w, badge_h = draw_pill_badge(
                    render_surface,
                    x=SCREEN_WIDTH // 2 - 75,
                    y=16,
                    text=slow_text,
                    font=assets.badge_font,
                    bg_color=(45, 38, 15, 235),
                    text_color=GOLD,
                    border_color=UI_ACCENT_GOLD
                )
                bar_ratio = slow_mo_timer / SLOW_MO_DURATION
                bar_w = int((badge_w - 16) * bar_ratio)
                pygame.draw.rect(render_surface, UI_ACCENT_GOLD, (SCREEN_WIDTH // 2 - 75 + 8, 16 + badge_h - 3, bar_w, 2), border_radius=1)

            # 8. Co giãn và trình chiếu lên màn hình thực tế (Scaling & Presentation)
            display_manager.present()
            self.clock.tick(FPS)

        sound_manager.stop_bgm()
        is_new_rec = score_manager.update_high_score(score, difficulty_name)
        return "QUIT", score, is_new_rec
