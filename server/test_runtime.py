#!/usr/bin/env python3
"""JALDORX KAGE X2 runtime check.

Run this on the KAGE X2 after setup_kage_x2.sh.
It checks the pieces required before enabling real video generation.
"""
import importlib.util
import platform
import subprocess


def command_version(command):
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT, timeout=10).strip()
    except Exception as exc:
        return f"NICHT VERFÜGBAR: {exc}"


print("=== JALDORX KI-Animator Runtime-Test ===")
print("Python:", platform.python_version())
print("System:", platform.platform())
print("NVIDIA:", command_version(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]))

for module in ("torch", "diffusers", "transformers", "accelerate", "huggingface_hub"):
    available = importlib.util.find_spec(module) is not None
    print(f"{module}: {'OK' if available else 'FEHLT'}")

try:
    import torch
    print("PyTorch:", torch.__version__)
    print("CUDA verfügbar:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("CUDA:", torch.version.cuda)
        print("GPU:", torch.cuda.get_device_name(0))
        print("VRAM GB:", round(torch.cuda.get_device_properties(0).total_memory / 1024**3, 2))
except Exception as exc:
    print("PyTorch-Test FEHLER:", exc)

print("=== Ende ===")
