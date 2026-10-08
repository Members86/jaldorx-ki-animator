#!/usr/bin/env python3
"""JALDORX local video engine adapter.

The JALDORX application owns this interface. A local model is only the
rendering engine behind it; the user does not need a separate UI.
"""
from pathlib import Path
import json
import subprocess


BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.json"


class VideoEngine:
    name = "JALDORX LOCAL AI"
    model_name = "Wan2.1-T2V-1.3B"

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self):
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

    def status(self):
        """Return engine information without starting a generation."""
        model = self.config.get("first_model_test", {})
        return {
            "name": self.name,
            "model": model.get("name", self.model_name),
            "mode": self.config.get("mode", "local"),
            "cloud_ai": self.config.get("cloud_ai", False),
            "ready": False,
            "message": "Lokaler Videomotor noch nicht installiert.",
        }

    def generate(self, *, prompt: str, duration: int, aspect_ratio: str,
                 image_path: str | None = None,
                 output_path: str = "output.mp4") -> str:
        """Generate one video with the installed local model.

        This method is intentionally the only place that needs to know how
        the selected model is executed.
        """
        if duration not in (5, 10):
            raise ValueError("Dauer muss 5 oder 10 Sekunden sein.")
        if aspect_ratio not in ("9:16", "16:9", "1:1"):
            raise ValueError("Ungültiges Seitenverhältnis.")
        if not prompt.strip():
            raise ValueError("Prompt darf nicht leer sein.")

        # Image-to-video wiring is intentionally kept behind the same adapter.
        # The concrete Wan pipeline is enabled only after the KAGE X2 runtime test.
        if image_path:
            mode = "image-to-video"
        else:
            mode = "text-to-video"
        raise NotImplementedError(
            f"JALDORX {mode}: lokaler Videomotor noch nicht installiert. "
            "Der Wan-Motor wird nach dem KAGE X2 Runtime-Test aktiviert."
        )


def model_available(command: str = "python3") -> bool:
    """Basic local runtime check used by the job server."""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False
