# 🏃‍♂️ Obstacle Runner

**Obstacle Runner** là một tựa game 2D sinh tồn được phát triển bằng **Python** và thư viện **Pygame**.

Người chơi điều khiển nhân vật di chuyển sang trái hoặc phải để né tránh các chướng ngại vật rơi từ phía trên màn hình. Trong quá trình chơi, người chơi có thể thu thập các vật phẩm hồi máu, đồng thời phải thích nghi với tốc độ chướng ngại vật ngày càng tăng để đạt được điểm số cao nhất.

---

## ✨ Tính năng nổi bật

### 🎮 Hệ thống Menu

Game được xây dựng với hệ thống giao diện gồm nhiều màn hình:

- **Main Menu** – Menu chính để bắt đầu game.
- **Difficulty Menu** – Lựa chọn mức độ khó.
- **Pause Menu** – Tạm dừng và tiếp tục trò chơi.
- **Game Over Screen** – Hiển thị kết quả khi người chơi thua.
- **Restart** – Cho phép bắt đầu lại một ván chơi.
- **Return to Menu** – Quay lại menu chính.

---

### 🎯 3 mức độ khó

Game cung cấp 3 mức độ khó:

| Mức độ | Mô tả |
|---|---|
| 🟢 Easy | Tốc độ chướng ngại vật ban đầu thấp |
| 🟡 Medium | Tốc độ chướng ngại vật ban đầu ở mức trung bình |
| 🔴 Hard | Tốc độ chướng ngại vật ban đầu cao |

Mức độ khó được lựa chọn trước khi bắt đầu game và ảnh hưởng trực tiếp đến tốc độ rơi ban đầu của chướng ngại vật.

---

### ❤️ Hệ thống sinh lực (HP)

Người chơi có tối đa **3 HP**.

Khi nhân vật va chạm với chướng ngại vật:

- HP bị giảm.
- Nhân vật chuyển sang trạng thái **I-frames** (Invincibility Frames).
- Trong thời gian này, nhân vật tạm thời không nhận thêm sát thương.
- Nhân vật có hiệu ứng nhấp nháy để biểu thị trạng thái bất tử tạm thời.
- Thời gian I-frames là **1.5 giây**.

Cơ chế này giúp tránh việc người chơi bị mất toàn bộ HP liên tục khi đứng quá gần một chướng ngại vật.

---

### 💚 Power-ups

Trong quá trình chơi có xác suất xuất hiện các vật phẩm hỗ trợ.

Power-up có màu xanh lá và rơi từ phía trên màn hình xuống.

Khi người chơi thu thập Power-up:

- Hồi lại **1 HP**.
- Được cộng thêm điểm.
- HP không vượt quá giới hạn tối đa.

---

### 📈 Độ khó tăng dần

Tốc độ của chướng ngại vật sẽ tăng theo điểm số.

Cứ mỗi **50 điểm**, tốc độ rơi của chướng ngại vật được tăng lên.

Điều này khiến game ngày càng khó khi người chơi đạt điểm cao, yêu cầu khả năng phản xạ và điều khiển tốt hơn.

---

## 🕹️ Gameplay

Gameplay chính của Obstacle Runner:

```text
                    ↓
              🟥 Obstacle
                    ↓
                    ↓
              🟥 Obstacle
                    ↓

        ←   🧍 Player   →

              🟩 Power-up
                    ↓

────────────────────────────
        Khu vực di chuyển
────────────────────────────
