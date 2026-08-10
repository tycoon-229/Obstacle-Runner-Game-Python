import pygame
import random

# =========================
# KHỞI TẠO
# =========================
pygame.init()

# Màn hình
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Obstacle Runner")

# FPS
clock = pygame.time.Clock()

# =========================
# MÀU SẮC
# =========================
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# =========================
# LOAD ẢNH
# =========================
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (800, 600))

player_img = pygame.image.load("player.png")
player_img = pygame.transform.scale(player_img, (70, 90))

obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (70, 90))

heart_img = pygame.image.load("heart.png")
heart_img = pygame.transform.scale(heart_img, (35, 35))

# =========================
# FONT
# =========================
big_font = pygame.font.SysFont(None, 72)
medium_font = pygame.font.SysFont(None, 42)
small_font = pygame.font.SysFont(None, 32)

# =========================
# TỐC ĐỘ GAME
# =========================
obs_speed = 5

# =========================
# CÁC LỚP ĐỐI TƯỢNG (OOP)
# =========================
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image.convert_alpha() # Hỗ trợ độ trong suốt cho hiệu ứng nhấp nháy
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = 0
        self.move_speed = 7
        
        # Hệ thống HP
        self.hp = 3
        self.invincible = False
        self.invincible_timer = 0

    def update(self):
        # Cập nhật vị trí
        self.rect.x += self.speed_x

        # Giới hạn màn hình
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            
        # Xử lý thời gian tàng hình (I-frames)
        if self.invincible:
            self.invincible_timer -= 1
            
            # Tạo hiệu ứng nhấp nháy bằng cách thay đổi độ trong suốt (alpha)
            if self.invincible_timer % 10 < 5:
                self.image.set_alpha(0) # Ẩn
            else:
                self.image.set_alpha(255) # Hiện
                
            # Hết thời gian tàng hình
            if self.invincible_timer <= 0:
                self.invincible = False
                self.image.set_alpha(255) # Đảm bảo nhân vật hiển thị lại bình thường

    def take_damage(self):
        # Hàm xử lý trừ máu, trả về True nếu bị trừ máu thành công
        if not self.invincible:
            self.hp -= 1
            self.invincible = True
            self.invincible_timer = 90 # Khoảng 1.5 giây tàng hình (ở mức 60 FPS)
            return True
        return False

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, current_speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 70)
        self.rect.y = random.randint(-700, -100)
        self.speed_y = current_speed

    def update(self):
        self.rect.y += self.speed_y
        
        if self.rect.top > screen_height:
            self.rect.y = random.randint(-500, -100)
            self.rect.x = random.randint(0, screen_width - 70)
            return True 
        return False

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Tạo một khối vuông màu xanh lá kích thước 40x40 làm vật phẩm hồi máu
        self.image = pygame.Surface((40, 40))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        
        self.rect.x = random.randint(0, screen_width - 40)
        self.rect.y = random.randint(-800, -100)
        self.speed_y = 4 # Vật phẩm sẽ rơi chậm hơn chướng ngại vật một chút

    def update(self):
        self.rect.y += self.speed_y
        
        # Tự hủy biến mất khỏi bộ nhớ khi rơi ra khỏi màn hình để tối ưu game
        if self.rect.top > screen_height:
            self.kill()

# =========================
# MENU CHÍNH
# =========================
def main_menu():
    menu = True
    while menu:
        screen.blit(background, (0, 0))

        title = big_font.render("OBSTACLE RUNNER", True, yellow)
        start_text = medium_font.render("Press SPACE to Start", True, white)
        quit_text = small_font.render("Press Q to Quit", True, white)

        screen.blit(title, (150, 180))
        screen.blit(start_text, (220, 300))
        screen.blit(quit_text, (300, 360))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                    difficulty_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# =========================
# MENU ĐỘ KHÓ
# =========================
def difficulty_menu():
    global obs_speed
    choosing = True
    while choosing:
        screen.blit(background, (0, 0))

        title = big_font.render("Choose Difficulty", True, yellow)
        easy = medium_font.render("1 - Easy", True, white)
        medium = medium_font.render("2 - Medium", True, white)
        hard = medium_font.render("3 - Hard", True, white)

        screen.blit(title, (170, 150))
        screen.blit(easy, (320, 260))
        screen.blit(medium, (290, 320))
        screen.blit(hard, (320, 380))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    obs_speed = 5
                    choosing = False
                    game_loop()
                elif event.key == pygame.K_2:
                    obs_speed = 8
                    choosing = False
                    game_loop()
                elif event.key == pygame.K_3:
                    obs_speed = 11
                    choosing = False
                    game_loop()

# =========================
# PAUSE GAME
# =========================
def pause_game():
    paused = True
    while paused:
        screen.blit(background, (0, 0))

        pause_text = big_font.render("PAUSED", True, red)
        continue_text = small_font.render("Press P to Continue", True, white)

        screen.blit(pause_text, (270, 220))
        screen.blit(continue_text, (260, 320))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        clock.tick(15)

# =========================
# GAME OVER
# =========================
def game_over(score):
    waiting = True
    while waiting:
        screen.blit(background, (0, 0))

        over_text = big_font.render("GAME OVER", True, red)
        score_text = medium_font.render(f"Score: {score}", True, white)
        restart_text = small_font.render("Press R to Restart", True, white)
        menu_text = small_font.render("Press M for Menu", True, white)
        quit_text = small_font.render("Press Q to Quit", True, white)

        screen.blit(over_text, (220, 180))
        screen.blit(score_text, (320, 270))
        screen.blit(restart_text, (280, 340))
        screen.blit(menu_text, (285, 390))
        screen.blit(quit_text, (300, 440))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_m:
                    main_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# =========================
# GAME LOOP
# =========================
def game_loop():
    # Khởi tạo các Group
    all_sprites = pygame.sprite.Group()
    obstacles_group = pygame.sprite.Group()
    powerups_group = pygame.sprite.Group() # Group quản lý vật phẩm

    # Tạo đối tượng Player
    player = Player(370, 480, player_img)
    all_sprites.add(player)

    # Khởi tạo chướng ngại vật
    current_speed = obs_speed
    for i in range(5):
        obs = Obstacle(obstacle_img, current_speed)
        all_sprites.add(obs)
        obstacles_group.add(obs)

    score = 0
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.speed_x = -player.move_speed
                elif event.key == pygame.K_RIGHT:
                    player.speed_x = player.move_speed
                elif event.key == pygame.K_p:
                    pause_game()

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    player.speed_x = 0

        # =========================
        # SPAWN VẬT PHẨM NGẪU NHIÊN
        # =========================
        # Có xác suất nhỏ xuất hiện vật phẩm rơi xuống ở mỗi khung hình
        if random.randint(1, 400) == 1:
            powerup = PowerUp()
            all_sprites.add(powerup)
            powerups_group.add(powerup)

        # =========================
        # CẬP NHẬT TRẠNG THÁI
        # =========================
        player.update()
        powerups_group.update()
        
        for obs in obstacles_group:
            if obs.update(): 
                score += 1
                if score > 0 and score % 50 == 0:
                    current_speed += 0.5
                    for o in obstacles_group:
                        o.speed_y = current_speed

        # =========================
        # XỬ LÝ VA CHẠM
        # =========================
        
        # 1. Va chạm với Chướng ngại vật
        hits = pygame.sprite.spritecollide(player, obstacles_group, False)
        if hits:
            # Nếu take_damage() trả về True (nghĩa là đang không tàng hình)
            if player.take_damage():
                if player.hp <= 0:
                    game_exit = True

        # 2. Va chạm với Vật phẩm (Power-ups)
        # Tham số True cuối cùng sẽ tự động xóa vật phẩm khỏi màn hình khi va chạm
        power_hits = pygame.sprite.spritecollide(player, powerups_group, True)
        for power in power_hits:
            if player.hp < 3:  # Giới hạn máu tối đa là 3
                player.hp += 1
            score += 2         # Thưởng thêm điểm khi ăn được vật phẩm

        # =========================
        # VẼ LÊN MÀN HÌNH
        # =========================
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)

        # Giao diện thông tin (UI)
        score_text = medium_font.render(f"Score: {score}", True, white)
        speed_text = small_font.render(f"Speed: {round(current_speed, 1)}", True, white)
        hp_text = medium_font.render(f"HP: {player.hp}", True, green)

        screen.blit(score_text, (20, 20))
        screen.blit(speed_text, (20, 60))
        
        for i in range(player.hp):
            # Tính toán tọa độ X để xếp các trái tim thành hàng ngang ở góc phải
            heart_x = (screen_width - 150) + (i * 40)
            heart_y = 20
            screen.blit(heart_img, (heart_x, heart_y))

        pygame.display.update()
        clock.tick(60)

    game_over(score)

# =========================
# START GAME
# =========================
if __name__ == "__main__":
    main_menu()