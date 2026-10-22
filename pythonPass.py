"""
Điểm khởi chạy tương thích ngược cho dự án Obstacle Runner.
Dự án đã được tái cấu trúc thành kiến trúc module hóa:
- config.py: Hằng số, màu sắc, tốc độ, đường dẫn tài nguyên
- assets.py: Quản lý nạp ảnh và font tập trung
- entities/: Chứa các lớp Player, Obstacle, PowerUp
- scenes/: Quản lý các màn hình Menu, Game, Pause, GameOver
- main.py: Vòng lặp chính và State Machine điều phối
"""
from main import main

if __name__ == "__main__":
    main()