#!/usr/bin/env python3
"""Download the configured JALDORX local video model.

This is a preparation tool only. It does not start video generation.
"""
from pathlib import Path
import json

try:
    from huggingface_hub import snapshot_download
except ImportError:
    raise SystemExit("huggingface_hub fehlt. Bitte zuerst setup_kage_x2.sh ausführen.")

ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
model = config["first_model_test"]["model_id"]
target = ROOT / "models" / "wan2.1-t2v-1.3b-diffusers"

print(f"Lade {model} nach {target} ...")
snapshot_download(repo_id=model, local_dir=str(target))
print("Modell lokal vorhanden.")
