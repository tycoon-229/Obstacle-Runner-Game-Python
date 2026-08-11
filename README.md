🏃‍♂️ Obstacle Runner
Một tựa game 2D sinh tồn nhịp độ nhanh được xây dựng bằng Python và thư viện Pygame. Người chơi sẽ điều khiển nhân vật né tránh các chướng ngại vật rơi từ trên xuống, thu thập vật phẩm hồi máu và cố gắng đạt điểm số cao nhất khi tốc độ game ngày càng tăng.

✨ Tính năng nổi bật
Hệ thống Menu hoàn chỉnh: Bao gồm Menu chính, Chọn độ khó, Tạm dừng (Pause) và Màn hình thua cuộc (Game Over).

3 Mức độ khó: Dễ (Easy), Trung bình (Medium) và Khó (Hard) ảnh hưởng trực tiếp đến tốc độ rơi ban đầu của chướng ngại vật.

Hệ thống Sinh lực (HP) & Tàng hình (I-frames): Người chơi có tối đa 3 HP. Khi trúng đòn, nhân vật sẽ nhấp nháy và tiến vào trạng thái "bất tử tạm thời" trong 1.5 giây để tránh bị nhận sát thương liên tục.

Vật phẩm hỗ trợ (Power-ups): Sẽ có xác suất xuất hiện vật phẩm màu xanh lá rơi xuống giúp hồi 1 HP và thưởng thêm điểm.

Độ khó tăng dần (Scaling difficulty): Cứ mỗi 50 điểm, chướng ngại vật sẽ rơi xuống nhanh hơn, đòi hỏi phản xạ nhạy bén hơn.

🛠 Yêu cầu hệ thống
Python 3.x

Thư viện pygame

🚀 Hướng dẫn cài đặt và Chạy game
Đảm bảo bạn đã cài đặt Python trên máy tính.

Cài đặt thư viện Pygame thông qua Terminal hoặc Command Prompt:

Bash
pip install pygame
Chuẩn bị tài nguyên (Assets): Đảm bảo bạn đã có sẵn các tệp hình ảnh sau nằm cùng một thư mục với file code. (Lưu ý: Game sẽ tự động scale lại kích thước, nhưng bạn nên chọn ảnh phù hợp):

background.png (Hình nền)

player.png (Nhân vật)

obstacle.png (Chướng ngại vật)

heart.png (Biểu tượng mạng/máu)

Mở Terminal tại thư mục chứa dự án và chạy lệnh:

Bash
python ten_file_cua_ban.py
🎮 Hướng dẫn điều khiển
Trong Menu & Giao diện:

Phím SPACE: Bắt đầu game (từ Menu chính)

Phím 1 / 2 / 3: Chọn mức độ khó tương ứng

Phím P: Tạm dừng (Pause) / Tiếp tục chơi

Phím R: Chơi lại ván mới (tại màn hình Game Over)

Phím M: Quay về Menu chính (tại màn hình Game Over)

Phím Q: Thoát game an toàn

Trong lúc chơi:

Mũi tên Trái (⬅️): Di chuyển nhân vật sang trái

Mũi tên Phải (➡️): Di chuyển nhân vật sang phải
