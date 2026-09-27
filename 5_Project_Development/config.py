"""Central configuration for LegalEase (paths, env vars, logo generation)."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")

IMAGE_DIR = BASE_DIR / "Image"
LOGO_PATH = IMAGE_DIR / "Logo.png"                  # dark text, used in DOCX / PDF (white paper)
WEB_LOGO_PATH = IMAGE_DIR / "inverseLogo.png"       # white text, used in the dark web UI

COMPANY_NAME = "LegalEase"
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."


def has_valid_api_key() -> bool:
    return bool(GEMINI_API_KEY) and GEMINI_API_KEY != "your_api_key_here"


def _load_font(size: int):
    from PIL import ImageFont

    for name in ("DejaVuSerif.ttf", "times.ttf", "Times New Roman.ttf", "georgia.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:  # very old Pillow
        return ImageFont.load_default()


def _draw_logo(path: Path, color) -> None:
    from PIL import Image, ImageDraw

    width, height = 640, 200
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    cx = 115  # scales of justice icon
    d.line([(cx, 40), (cx, 150)], fill=color, width=6)
    d.rectangle([cx - 40, 150, cx + 40, 160], fill=color)
    d.line([(cx - 70, 60), (cx + 70, 60)], fill=color, width=6)
    d.ellipse([cx - 9, 31, cx + 9, 49], fill=color)
    for px in (cx - 70, cx + 70):
        d.line([(px, 60), (px - 30, 115)], fill=color, width=3)
        d.line([(px, 60), (px + 30, 115)], fill=color, width=3)
        d.chord([px - 32, 95, px + 32, 135], 0, 180, fill=color)

    font = _load_font(72)
    try:
        d.text((215, height // 2), COMPANY_NAME, font=font, fill=color, anchor="lm")
    except (ValueError, TypeError):
        d.text((215, 70), COMPANY_NAME, font=font, fill=color)
    img.save(path)


def ensure_logos() -> None:
    """Create placeholder logos if you have not added your own to /Image."""
    IMAGE_DIR.mkdir(exist_ok=True)
    if not LOGO_PATH.exists():
        _draw_logo(LOGO_PATH, (20, 30, 60, 255))
    if not WEB_LOGO_PATH.exists():
        _draw_logo(WEB_LOGO_PATH, (255, 255, 255, 255))
