"""
Quản lý đọc và ghi điểm cao (High Score) vào file JSON.
Hỗ trợ lưu điểm kỷ lục theo từng mức độ khó và kỷ lục cao nhất mọi thời đại.
"""
import json
import os
from config import BASE_DIR

SCORE_FILE = os.path.join(BASE_DIR, "highscore.json")

class ScoreManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ScoreManager, cls).__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        self.data = {
            "EASY": 0,
            "MEDIUM": 0,
            "HARD": 0,
            "ALL_TIME_BEST": 0
        }
        if os.path.exists(SCORE_FILE):
            try:
                with open(SCORE_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    if isinstance(loaded, dict):
                        self.data.update(loaded)
            except Exception:
                pass

    def _save(self):
        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4)
        except Exception:
            pass

    def get_high_score(self, difficulty="ALL_TIME_BEST") -> int:
        """Lấy điểm kỷ lục theo mức độ khó hoặc kỷ lục chung."""
        return self.data.get(difficulty, 0)

    def update_high_score(self, score: int, difficulty: str) -> bool:
        """
        Cập nhật điểm cao mới nếu vượt qua kỷ lục cũ.
        Trả về True nếu xác lập kỷ lục mới, ngược lại False.
        """
        is_new_record = False
        if score > self.data.get(difficulty, 0):
            self.data[difficulty] = score
            is_new_record = True

        if score > self.data.get("ALL_TIME_BEST", 0):
            self.data["ALL_TIME_BEST"] = score
            is_new_record = True

        if is_new_record:
            self._save()

        return is_new_record

score_manager = ScoreManager()
