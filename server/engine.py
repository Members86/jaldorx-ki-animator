#!/usr/bin/env python3
"""JALDORX local video engine adapter.

This module is deliberately model-agnostic. The actual local video model
(Wan/LTX/etc.) will be plugged in on the KAGE X2 later.
"""

from pathlib import Path
import subprocess


class VideoEngine:
    name = "JALDORX LOCAL AI"

    def generate(self, *, prompt: str, duration: int, aspect_ratio: str,
                 image_path: str | None = None, output_path: str = "output.mp4") -> str:
        """Generate one video and return its output path.

        The concrete local model implementation will be connected here.
        No cloud API is used.
        """
        raise NotImplementedError(
            "Lokale Video-KI ist noch nicht installiert. "
            "Auf dem KAGE X2 wird hier der gewählte lokale Motor angeschlossen."
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
