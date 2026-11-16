"""Package PlatformIO ESP32 build artifacts for ESP Web Tools."""
import json
import os
import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
build = root / ".pio" / "build" / "esp32-2432s028r"
site = root / "web-installer"
dest = site / "firmware"
dest.mkdir(parents=True, exist_ok=True)

platformio_root = Path(os.environ.get("PLATFORMIO_CORE_DIR", Path.home() / ".platformio"))
boot_app0 = platformio_root / "packages" / "framework-arduinoespressif32" / "tools" / "partitions" / "boot_app0.bin"
parts = [
    ("bootloader.bin", build / "bootloader.bin", 0x1000),
    ("partitions.bin", build / "partitions.bin", 0x8000),
    ("boot_app0.bin", boot_app0, 0xE000),
    ("firmware.bin", build / "firmware.bin", 0x10000),
]
for name, src, offset in parts:
    if not src.is_file() or src.stat().st_size == 0:
        raise FileNotFoundError(f"Build artifact missing: {src}")
    if name in ("bootloader.bin", "firmware.bin") and src.read_bytes()[:1] != bytes([0xE9]):
        raise ValueError(f"Invalid ESP32 image: {src}")
    shutil.copy2(src, dest / name)
    print(f"{name}: {src.stat().st_size} bytes @ {offset:#x}")

manifest = {
    "name": "CYD Pixel Aquarium",
    "version": os.environ.get("GITHUB_SHA", "local")[:12],
    "new_install_prompt_erase": True,
    "builds": [{
        "chipFamily": "ESP32",
        "parts": [{"path": f"firmware/{name}", "offset": offset} for name, _, offset in parts]
    }]
}
(site / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
