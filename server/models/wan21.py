#!/usr/bin/env python3
"""Wan 2.1 adapter used internally by JALDORX KI-Animator.

The adapter follows the official Hugging Face Diffusers WanPipeline.
It is intentionally lazy: importing JALDORX does not load the large model.
"""
from pathlib import Path
import torch


class Wan21Generator:
    MODEL_ID = "Wan-AI/Wan2.1-T2V-1.3B-Diffusers"

    def __init__(self, model_path: str | None = None):
        self.model_path = Path(model_path) if model_path else Path(__file__).resolve().parents[1] / "models" / "wan2.1-t2v-1.3b-diffusers"
        self.pipe = None

    def status(self) -> dict:
        model_present = self.model_path.exists()
        cuda = bool(torch.cuda.is_available())
        vram_gb = None
        gpu = None
        if cuda:
            props = torch.cuda.get_device_properties(0)
            gpu = props.name
            vram_gb = round(props.total_memory / 1024**3, 2)
        return {
            "model": self.MODEL_ID,
            "model_present": model_present,
            "cuda": cuda,
            "gpu": gpu,
            "vram_gb": vram_gb,
            "ready": model_present and cuda,
        }

    def load(self):
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA ist nicht verfügbar.")
        if not self.model_path.exists():
            raise FileNotFoundError(f"Wan-Modell fehlt: {self.model_path}")

        from diffusers import AutoencoderKLWan, WanPipeline
        from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler

        vae = AutoencoderKLWan.from_pretrained(
            str(self.model_path),
            subfolder="vae",
            torch_dtype=torch.float32,
        )
        self.pipe = WanPipeline.from_pretrained(
            str(self.model_path),
            vae=vae,
            torch_dtype=torch.bfloat16,
        )
        self.pipe.scheduler = UniPCMultistepScheduler.from_config(
            self.pipe.scheduler.config,
            flow_shift=3.0,
        )
        self.pipe.to("cuda")
        return self.pipe

    def generate(self, prompt: str, output_path: str, frames: int = 81,
                 width: int = 480, height: int = 832, steps: int = 30):
        if self.pipe is None:
            self.load()

        from diffusers.utils import export_to_video

        result = self.pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_frames=frames,
            num_inference_steps=steps,
        )
        export_to_video(result.frames[0], output_path, fps=16)
        return output_path
