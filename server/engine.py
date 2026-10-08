#!/usr/bin/env python3
"""JALDORX local video engine.

This is the single internal bridge between the JALDORX job server and the
selected local video model. The user-facing application never needs to know
which model is underneath.
"""
from pathlib import Path
import json
import torch

from models.wan21 import Wan21Generator

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


class VideoEngine:
    name = "JALDORX LOCAL AI"

    def __init__(self):
        self.config = self._load_config()
        model_path = self.config.get("first_model_test", {}).get(
            "local_path", "models/wan2.1-t2v-1.3b-diffusers"
        )
        self.wan = Wan21Generator(BASE_DIR / model_path)

    def _load_config(self):
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def status(self):
        info = self.wan.status()
        return {
            "name": self.name,
            "model": info["model"],
            "mode": "local",
            "cloud_ai": False,
            "gpu": info["gpu"],
            "vram_gb": info["vram_gb"],
            "model_present": info["model_present"],
            "cuda": info["cuda"],
            "ready": info["ready"],
            "message": "Bereit" if info["ready"] else "Lokaler Motor noch nicht bereit.",
        }

    def generate(self, *, prompt: str, duration: int, aspect_ratio: str,
                 image_path: str | None = None,
                 output_path: str = "output.mp4") -> str:
        if duration not in (5, 10):
            raise ValueError("Dauer muss 5 oder 10 Sekunden sein.")
        if aspect_ratio not in ("9:16", "16:9", "1:1"):
            raise ValueError("Ungültiges Seitenverhältnis.")
        if not prompt.strip():
            raise ValueError("Prompt darf nicht leer sein.")
        if image_path:
            raise NotImplementedError(
                "Produktbild-Modus wird nach dem ersten stabilen Text-zu-Video-Test aktiviert."
            )

        if not self.wan.status()["ready"]:
            raise RuntimeError("Wan 2.1 ist auf dem KAGE X2 noch nicht bereit.")

        # 16 fps: 5 sec = 81 frames, 10 sec = 161 frames.
        frames = duration * 16 + 1

        # First stable portrait test. The model is evaluated at 480p-class
        # dimensions before we optimize other aspect ratios.
        width, height = 480, 832
        if aspect_ratio == "16:9":
            width, height = 832, 480
        elif aspect_ratio == "1:1":
            width, height = 480, 480

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        return self.wan.generate(
            prompt=prompt,
            output_path=output_path,
            frames=frames,
            width=width,
            height=height,
            steps=int(self.config.get("first_model_test", {}).get("default_steps", 30)),
        )


def model_available() -> bool:
    return torch.cuda.is_available()
