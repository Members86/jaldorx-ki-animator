#!/usr/bin/env bash
set -euo pipefail

# JALDORX KI-Animator – KAGE X2 local setup
# Run this on the KAGE X2 after Python/NVIDIA drivers are ready.

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install --upgrade torch torchvision --index-url https://download.pytorch.org/whl/cu128
python -m pip install --upgrade diffusers transformers accelerate ftfy imageio imageio-ffmpeg

mkdir -p models output

echo
echo "JALDORX KI-Animator – Grundinstallation fertig."
echo "Nächster Schritt: Wan2.1-Modell lokal laden und ersten Testclip erzeugen."
echo "Model: Wan-AI/Wan2.1-T2V-1.3B-Diffusers"
echo "Kein Cloud-API-Key erforderlich."
