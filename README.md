# 🏃‍♂️ Obstacle Runner

**Obstacle Runner** là một tựa game 2D sinh tồn được phát triển bằng **Python** và thư viện **Pygame**, được thiết kế với phong cách đồ họa **Modern Cyber & Glassmorphism UI**, hỗ trợ **phóng to Full HD 1920x1080 / Toàn màn hình F11**, hệ thống **âm thanh SFX & BGM sống động**, cùng cơ chế **di chuyển tự do 4 hướng**.

---

## ✨ Tính năng nổi bật mới cập nhật

### 🕹️ Di Chuyển Tự Do 4 Hướng (Free 4-Way Movement)
- Người chơi có thể tự do bay lượn và né chướng ngại vật theo cả 4 hướng: **Trái, Phải, Lên, Xuống**.
- Hỗ trợ linh hoạt cả 2 hệ phím:
  - Cụm phím chữ: **`W` (Lên)**, **`S` (Xuống)**, **`A` (Trái)**, **`D` (Phải)**.
  - Cụm phím mũi tên: **`↑`**, **`↓`**, **`←`**, **`→`**.
- Giới hạn biên thông minh giúp nhân vật không bao giờ bị bay ra ngoài khung hình.

---

### 🖥️ Phóng To Màn Hình & Cài Đặt Độ Phân Giải (Display Scaling & Fullscreen)
- **Công nghệ Virtual Canvas**: Trò chơi render trên canvas ảo chuẩn `800x600` rồi tự động scale mượt mà lên bất kỳ độ phân giải nào mà không làm méo hình.
- **Tùy chọn độ phân giải linh hoạt**:
  - `800 x 600` (Chuẩn mặc định)
  - `1200 x 900` (Phóng to 1.5x)
  - `1600 x 1200` (Độ nét cao HD 2.0x)
  - `1920 x 1080` (Chuẩn Full HD màn ảnh rộng 16:9 với thanh viền cân đối)
- **Toàn màn hình (Fullscreen)**: Nhấn **`F11`** bất kỳ lúc nào để chuyển đổi tức thì giữa chế độ cửa sổ và toàn màn hình.
- **Cửa sổ co giãn tự do**: Bạn cũng có thể dùng chuột kéo giãn mép cửa sổ tùy ý (`RESIZABLE`).

---

### 🔊 Hệ Thống Âm Thanh Đa Phương Tiện (Audio & SFX)
- **Tự động tổng hợp âm thanh**: Game tự động tạo các file âm thanh chuẩn 16-bit WAV thuần Python:
  - 💥 **Va chạm (Hit)**: Tiếng va đập trầm đục khi trúng chướng ngại vật.
  - 💚 **Hồi máu (Heal)**: Hợp âm ngân vang tươi sáng khi nhặt item máu.
  - 🛡️ **Khiên bảo vệ (Shield)**: Tiếng quét năng lượng sci-fi khi nhận khiên.
  - ⚡ **Khiên vỡ (Shield Break)**: Âm thanh vỡ năng lượng cảnh báo khi bị đòn đánh phá khiên.
  - ⏳ **Làm chậm (Slow-Mo)**: Âm thanh bẻ cong thời gian khi ăn đồng hồ.
  - 🚨 **Còi báo động (Warning)**: Hai hồi còi cấp bách cảnh báo thiên thạch lao xuống.
  - 🖱️ **Click UI**: Âm thanh nhấn nút công nghệ cao.
  - ☠️ **Game Over**: Giai điệu kết thúc trận đấu.
  - 🎵 **Nhạc nền (BGM)**: Nhạc nền điện tử Arcade 8-bit sôi động nhịp điệu 130 BPM.
- **Bật/Tắt âm thanh nhanh**: Nhấn phím **`M`** để bật hoặc tắt âm thanh bất cứ lúc nào.

---

### 💎 Giao Diện Hiện Đại (Modern Glassmorphism UI)
- Toàn bộ bảng Menu, Modal Tạm Dừng, Thẻ Kết Quả (Game Over) và HUD được đóng khung trong các thẻ bán trong suốt có viền phản quang hiện đại.
- Nút bấm hỗ trợ cả chuột (có hiệu ứng hover animation nhấc 2px và phát quang) lẫn phím tắt.
- Rung chấn màn hình (Screen Shake) và thông báo chữ nổi bay (Floating Text) khi va chạm hoặc nhặt đồ.

---

### ☄️ Các Loại Chướng Ngại Vật Đa Dạng
- 🪨 **Normal**: Rơi thẳng đứng từ trên xuống.
- 〰️ **Wavy / Zigzag**: Tông màu tím năng lượng, lượn sóng ziczac theo hàm `sin(y)`.
- 🚀 **Fast Meteor**: Tông màu đỏ lửa rực cháy, rơi siêu tốc kèm cảnh báo `[ ! ]` và dải laser trước 1.15s.

---

### 🎯 Cải Thiện Hitbox Chuẩn Xác (Pixel-Perfect Collision)
- Sử dụng **`pygame.mask`** kết hợp `pygame.sprite.collide_mask` để triệt tiêu 100% hiện tượng va chạm ảo do khoảng trống trong suốt của ảnh PNG.

---

### 🏆 Hệ Thống Điểm Kỷ Lục (High Score)
- Tự động lưu và cập nhật điểm cao nhất vào file `highscore.json` theo từng chế độ độ khó.

---

## 🏗️ Cấu trúc thư mục dự án

```text
Obstacle-Runner-Game-Python/
│
├── config.py                 # Hằng số, kích thước, bảng màu hiện đại, thông số game
├── assets.py                 # Quản lý nạp ảnh, biến thể màu & font chữ Segoe UI
│
├── assets/
│   └── sounds/               # Thư mục âm thanh tự động tổng hợp (WAV)
│
├── ui/                       # Thư viện thành phần giao diện hiện đại
│   ├── button.py             # UIButton với hover animation, âm thanh click và phím tắt
│   ├── glass_panel.py        # Vẽ thẻ kính mờ (Glassmorphism) và Pill Badges
│   └── particles.py          # Bụi sáng lơ lửng và pháo hoa kỷ lục
│
├── entities/                 # Các thực thể đối tượng trong trò chơi
│   ├── player.py             # Người chơi (di chuyển tự do 4 hướng, máu, khiên, pixel-mask)
│   ├── obstacle.py           # Chướng ngại vật: Normal, Wavy ziczac, FastMeteor cảnh báo !
│   ├── powerup.py            # Vật phẩm (Heal, Shield, Slow-Mo)
│   └── scrolling_background.py # Nền cuộn dọc liên tục
│
├── scenes/                   # Quản lý các màn hình trò chơi
│   ├── menu_scene.py         # Main Menu & Difficulty Menu (Nút chỉnh Scale, Sound, Start)
│   ├── game_scene.py         # Màn chơi chính, Top Glass HUD, Screen Shake, 4-way move
│   ├── pause_scene.py        # Modal tạm dừng kính mờ (chỉnh Scale & Sound trong game)
│   └── game_over_scene.py    # Thẻ kết quả, so sánh điểm số & nút thao tác
│
├── utils/                    # Tiện ích bổ trợ
│   ├── score_manager.py      # Đọc và ghi High Score vào highscore.json
│   ├── sound_manager.py      # Quản lý phát SFX, BGM và bật/tắt tiếng (Mute)
│   └── display_manager.py    # Virtual Canvas Scaler, phóng to 1920x1080 & F11 Fullscreen
│
├── main.py                   # Điểm khởi chạy chính & Scene State Machine
└── pythonPass.py             # Cầu nối tương thích ngược đến main.py
```

---

## 🚀 Cách chạy Game

Chạy bằng lệnh:
```bash
python main.py
```
*(Hoặc chạy qua file cũ `python pythonPass.py`)*

### 🎮 Bảng phím tắt điều khiển:
- **Di chuyển**: `W / A / S / D` hoặc các phím mũi tên `↑ / ↓ / ← / →`.
- **Tạm dừng**: `P`.
- **Bật/Tắt âm thanh**: `M`.
- **Bật/Tắt Toàn màn hình**: `F11`.
- **Đổi tỉ lệ màn hình nhanh (ở Menu hoặc Pause)**: `TAB` hoặc click trực tiếp vào nút SCALE.
