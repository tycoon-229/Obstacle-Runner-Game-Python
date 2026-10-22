"""
Hệ thống âm thanh đa phương tiện cho trò chơi.
Tự động tổng hợp và lưu trữ các hiệu ứng âm thanh arcade 16-bit 44.1kHz (WAV)
bao gồm tiếng va chạm, nhặt vật phẩm, cảnh báo thiên thạch, nhạc nền (BGM) và UI click.
"""
import os
import math
import wave
import struct
import pygame
from config import BASE_DIR

SOUNDS_DIR = os.path.join(BASE_DIR, "assets", "sounds")

class SoundSynthesizer:
    """Tạo file WAV chuẩn 16-bit Mono 44.1kHz thuần Python không phụ thuộc thư viện ngoài."""
    SAMPLE_RATE = 44100

    @classmethod
    def _write_wav(cls, filepath, samples):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with wave.open(filepath, "w") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(cls.SAMPLE_RATE)
            packed = bytearray()
            for s in samples:
                val = max(-32767, min(32767, int(s)))
                packed.extend(struct.pack("<h", val))
            f.writeframes(packed)

    @classmethod
    def generate_all_sounds(cls):
        hit_path = os.path.join(SOUNDS_DIR, "hit.wav")
        if not os.path.exists(hit_path):
            cls._create_hit(hit_path)

        heal_path = os.path.join(SOUNDS_DIR, "heal.wav")
        if not os.path.exists(heal_path):
            cls._create_heal(heal_path)

        shield_path = os.path.join(SOUNDS_DIR, "shield.wav")
        if not os.path.exists(shield_path):
            cls._create_shield(shield_path)

        shield_break_path = os.path.join(SOUNDS_DIR, "shield_break.wav")
        if not os.path.exists(shield_break_path):
            cls._create_shield_break(shield_break_path)

        slow_mo_path = os.path.join(SOUNDS_DIR, "slow_mo.wav")
        if not os.path.exists(slow_mo_path):
            cls._create_slow_mo(slow_mo_path)

        warning_path = os.path.join(SOUNDS_DIR, "warning.wav")
        if not os.path.exists(warning_path):
            cls._create_warning(warning_path)

        click_path = os.path.join(SOUNDS_DIR, "click.wav")
        if not os.path.exists(click_path):
            cls._create_click(click_path)

        game_over_path = os.path.join(SOUNDS_DIR, "game_over.wav")
        if not os.path.exists(game_over_path):
            cls._create_game_over(game_over_path)

        bgm_path = os.path.join(SOUNDS_DIR, "bgm.wav")
        if not os.path.exists(bgm_path):
            cls._create_bgm(bgm_path)

    @classmethod
    def _create_hit(cls, filepath):
        # Tiếng thình thịch trầm + decay nhanh khi trúng đạn
        duration = 0.18
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            freq = 240 * (1 - t / duration) + 40
            env = (1 - t / duration) ** 2
            val = math.sin(2 * math.pi * freq * t) * env * 24000
            samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_heal(cls, filepath):
        # Hợp âm đi lên tươi sáng (C5 -> E5 -> G5 -> C6)
        notes = [523.25, 659.25, 783.99, 1046.50]
        note_dur = 0.06
        samples = []
        for freq in notes:
            num = int(cls.SAMPLE_RATE * note_dur)
            for i in range(num):
                t = i / cls.SAMPLE_RATE
                env = math.sin(math.pi * (i / num))
                val = math.sin(2 * math.pi * freq * t) * env * 18000
                samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_shield(cls, filepath):
        # Tiếng kích hoạt khiên năng lượng tần số quét tăng dần
        duration = 0.28
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            freq = 300 + (t / duration) ** 2 * 900
            env = math.sin(math.pi * (t / duration))
            val = math.sin(2 * math.pi * freq * t) * env * 19000
            samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_shield_break(cls, filepath):
        # Tiếng vỡ khiên thủy tinh / kim loại nứt
        duration = 0.22
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            env = (1 - t / duration) ** 3
            val = (math.sin(2 * math.pi * 1200 * t) + math.sin(2 * math.pi * 780 * t)) * env * 15000
            samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_slow_mo(cls, filepath):
        # Tiếng bẻ cong không gian thời gian (quét tần số giảm dần)
        duration = 0.35
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            freq = 800 * (1 - t / duration) + 120
            env = math.sin(math.pi * (t / duration))
            val = math.sin(2 * math.pi * freq * t) * env * 20000
            samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_warning(cls, filepath):
        # Còi báo động hai nốt cao liên tiếp cho thiên thạch
        samples = []
        for _ in range(2):
            num = int(cls.SAMPLE_RATE * 0.08)
            for i in range(num):
                t = i / cls.SAMPLE_RATE
                val = math.sin(2 * math.pi * 950 * t) * 22000
                samples.append(val)
            # Im lặng 0.04s
            samples.extend([0] * int(cls.SAMPLE_RATE * 0.04))
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_click(cls, filepath):
        duration = 0.035
        num_samples = int(cls.SAMPLE_RATE * duration)
        samples = []
        for i in range(num_samples):
            t = i / cls.SAMPLE_RATE
            env = 1 - t / duration
            val = math.sin(2 * math.pi * 1400 * t) * env * 16000
            samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_game_over(cls, filepath):
        # 3 nốt trầm đi xuống báo hiệu thất bại
        notes = [440.0, 392.0, 329.63, 261.63]
        dur = 0.15
        samples = []
        for freq in notes:
            num = int(cls.SAMPLE_RATE * dur)
            for i in range(num):
                t = i / cls.SAMPLE_RATE
                env = 1 - i / num
                val = math.sin(2 * math.pi * freq * t) * env * 19000
                samples.append(val)
        cls._write_wav(filepath, samples)

    @classmethod
    def _create_bgm(cls, filepath):
        # Giai điệu điện tử Arcade 8-bit lặp tuần hoàn nhịp điệu 130 BPM (~3.7s loop)
        bpm = 130
        beat_dur = 60.0 / bpm / 2  # Eighth note
        melody = [
            261.63, 293.66, 329.63, 392.0, 523.25, 392.0, 329.63, 293.66,
            261.63, 329.63, 392.0, 523.25, 659.25, 523.25, 392.0, 329.63
        ]
        samples = []
        for freq in melody:
            num = int(cls.SAMPLE_RATE * beat_dur)
            for i in range(num):
                t = i / cls.SAMPLE_RATE
                env = (1 - (i / num) * 0.4) * (0.8 if i < num - 300 else (num - i) / 300)
                # Sóng vuông mềm 8-bit
                sine = math.sin(2 * math.pi * freq * t)
                wave_val = 1.0 if sine > 0 else -1.0
                bass = math.sin(2 * math.pi * (freq / 2) * t) * 0.4
                val = (wave_val * 0.5 + bass) * env * 8500
                samples.append(val)
        cls._write_wav(filepath, samples)


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def init(self):
        if self.initialized:
            return

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(44100, -16, 2, 512)
        except Exception:
            pass

        # Tạo file âm thanh nếu chưa có
        SoundSynthesizer.generate_all_sounds()

        self.sounds = {}
        self.muted = False
        self.sfx_volume = 0.8
        self.bgm_volume = 0.45

        sound_keys = ["hit", "heal", "shield", "shield_break", "slow_mo", "warning", "click", "game_over"]
        for k in sound_keys:
            path = os.path.join(SOUNDS_DIR, f"{k}.wav")
            if os.path.exists(path):
                try:
                    snd = pygame.mixer.Sound(path)
                    snd.set_volume(self.sfx_volume)
                    self.sounds[k] = snd
                except Exception:
                    pass

        self.bgm_path = os.path.join(SOUNDS_DIR, "bgm.wav")
        self.initialized = True

    def play(self, sound_name):
        if self.muted:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            snd.play()

    def start_bgm(self):
        if not self.initialized:
            return
        try:
            if os.path.exists(self.bgm_path):
                pygame.mixer.music.load(self.bgm_path)
                pygame.mixer.music.set_volume(0 if self.muted else self.bgm_volume)
                pygame.mixer.music.play(-1)
        except Exception:
            pass

    def stop_bgm(self):
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def toggle_mute(self):
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.bgm_volume)
        return self.muted

sound_manager = SoundManager()
