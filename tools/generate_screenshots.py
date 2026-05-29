from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900
BG = "#F5F5F5"
PRIMARY = "#1E2A38"
ACCENT = "#A3B18A"
TEXT = "#222222"
MUTED = "#6C7075"
CARD = "#FFFFFF"
BORDER = "#D9D9D9"
SOFT = "#EEF1EF"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arial.ttf",
    ]
    if bold:
        candidates.insert(0, r"C:\Windows\Fonts\seguisb.ttf")
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


TITLE = font(46, True)
SUBTITLE = font(18)
SECTION = font(20, True)
BODY = font(16)
SMALL = font(13)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill, radius: int = 18, outline=None, width: int = 1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], lines: list[str], font_obj, fill, spacing: int = 6):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + spacing


def draw_chip(draw, x, y, label, active=False):
    fill = PRIMARY if active else "#E7EAE7"
    text_fill = "#FFFFFF" if active else PRIMARY
    rounded(draw, (x, y, x + 122, y + 42), fill=fill, radius=12)
    bbox = draw.textbbox((0, 0), label, font=SMALL)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (122 - tw) / 2, y + (42 - th) / 2 - 1), label, font=SMALL, fill=text_fill)


def draw_slider(draw, x, y, value):
    draw.rounded_rectangle((x, y + 20, x + 520, y + 28), radius=4, fill="#DCE1DC")
    fill_w = int(520 * (value / 25))
    draw.rounded_rectangle((x, y + 20, x + fill_w, y + 28), radius=4, fill=ACCENT)
    knob_x = x + fill_w
    draw.ellipse((knob_x - 12, y + 11, knob_x + 12, y + 35), fill=PRIMARY, outline=CARD)
    draw.text((x, y), "Caesar Shift", font=BODY, fill=TEXT)
    draw.text((x + 455, y - 3), f"Shift: {value}", font=SMALL, fill=PRIMARY)


def draw_card(draw, box, title):
    rounded(draw, box, fill=CARD, outline=BORDER, radius=22)
    draw.text((box[0] + 28, box[1] + 22), title, font=SECTION, fill=PRIMARY)


def draw_history_item(draw, x, y, mode, cipher, original, result, time):
    rounded(draw, (x, y, x + 430, y + 110), fill="#FBFCFB", outline=BORDER, radius=14)
    draw.text((x + 16, y + 12), f"[{mode}] {cipher}", font=BODY, fill=PRIMARY)
    draw.text((x + 16, y + 42), f"{original} \u2192 {result}", font=SMALL, fill=ACCENT)
    draw.text((x + 16, y + 82), time, font=SMALL, fill=MUTED)


def draw_window(state: dict[str, str], filename: str) -> None:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((38, 32), "CipherFlow", font=TITLE, fill=PRIMARY)
    draw.text((38, 94), "Real-time text encryption utility", font=SUBTITLE, fill=MUTED)

    draw_card(draw, (32, 140, 700, 860), "Controls")
    draw_card(draw, (728, 140, 1408, 860), "Output")

    # Left side
    x = 62
    y = 194
    draw.text((x, y), "Mode", font=BODY, fill=TEXT)
    draw_chip(draw, x, y + 32, "Encrypt", active=state["mode"] == "Encrypt")
    draw_chip(draw, x + 136, y + 32, "Decrypt", active=state["mode"] == "Decrypt")

    y += 120
    draw.text((x, y), "Input Text", font=BODY, fill=TEXT)
    rounded(draw, (x, y + 34, x + 576, y + 260), fill="#FFFFFF", outline=BORDER, radius=16)
    if state["input"]:
        text_block(draw, (x + 18, y + 54), state["input"].split("\n"), BODY, TEXT, spacing=8)
    else:
        draw.text((x + 18, y + 56), "Type or paste text here...", font=BODY, fill="#9AA0A6")

    y += 300
    draw.text((x, y), "Cipher", font=BODY, fill=TEXT)
    rounded(draw, (x, y + 34, x + 576, y + 76), fill=SOFT, outline=BORDER, radius=12)
    draw.text((x + 18, y + 45), state["cipher"], font=BODY, fill=PRIMARY)

    y += 108
    if state["cipher"] == "Caesar Cipher":
        draw_slider(draw, x, y, int(state["shift"]))
    else:
        draw.text((x, y), "Key", font=BODY, fill=TEXT)
        rounded(draw, (x, y + 34, x + 576, y + 76), fill="#FFFFFF", outline=BORDER, radius=12)
        draw.text((x + 18, y + 45), state["key"], font=BODY, fill=PRIMARY)
        if state["hint"]:
            draw.text((x, y + 92), state["hint"], font=SMALL, fill=ACCENT)

    # Generate button
    rounded(draw, (x, 752, x + 576, 796), fill=PRIMARY, radius=12)
    label = "Generate Key"
    bbox = draw.textbbox((0, 0), label, font=BODY)
    draw.text((x + (576 - (bbox[2] - bbox[0])) / 2, 763), label, font=BODY, fill="#FFFFFF")
    if state["validation"]:
        draw.text((x, 812), state["validation"], font=SMALL, fill="#B85C5C")

    # Right side
    x = 760
    y = 194
    draw.text((x, y), "Live Output", font=BODY, fill=TEXT)
    rounded(draw, (x, y + 34, x + 580, y + 260), fill="#FAFAFA", outline=BORDER, radius=16)
    out = state["output"] or " "
    text_block(draw, (x + 18, y + 54), out.split("\n"), BODY, TEXT, spacing=8)

    rounded(draw, (x, 488, x + 272, 532), fill="#EEF1EF", radius=12)
    rounded(draw, (x + 308, 488, x + 580, 532), fill="#EEF1EF", radius=12)
    draw.text((x + 70, 499), "Copy Output", font=BODY, fill=PRIMARY)
    draw.text((x + 400, 499), "Clear All", font=BODY, fill=PRIMARY)
    if state["copied"]:
        draw.text((x, 548), state["copied"], font=SMALL, fill=ACCENT)

    draw.text((x, 606), "History", font=BODY, fill=TEXT)
    history = state["history"]
    for idx, item in enumerate(history):
        draw_history_item(draw, x, 642 + idx * 122, **item)

    img.save(OUT_DIR / filename)


def build_states():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "main-screen.png": {
            "mode": "Encrypt",
            "cipher": "Caesar Cipher",
            "shift": 3,
            "input": "hello world",
            "output": "khoor zruog",
            "key": "",
            "hint": "",
            "validation": "",
            "copied": "",
            "history": [
                {"mode": "Encrypt", "cipher": "Caesar", "original": "hello", "result": "khoor", "time": now},
                {"mode": "Decrypt", "cipher": "Caesar", "original": "khoor", "result": "hello", "time": now},
            ],
        },
        "encrypt-mode.png": {
            "mode": "Encrypt",
            "cipher": "Vigen\u00e8re Cipher",
            "shift": 3,
            "input": "team meeting at noon",
            "output": "xqgx gqbbvxo qc rsvf",
            "key": "CLEAN",
            "hint": "Generated alphabetic key.",
            "validation": "",
            "copied": "Copied!",
            "history": [
                {"mode": "Encrypt", "cipher": "Vigen\u00e8re", "original": "team meeting at noon", "result": "xqgx gqbbvxo qc rsvf", "time": now},
                {"mode": "Encrypt", "cipher": "Caesar", "original": "notes", "result": "qrzhv", "time": now},
            ],
        },
        "decrypt-mode.png": {
            "mode": "Decrypt",
            "cipher": "Caesar Cipher",
            "shift": 5,
            "input": "mjqqt, btwqi!",
            "output": "hello, world!",
            "key": "",
            "hint": "",
            "validation": "",
            "copied": "",
            "history": [
                {"mode": "Decrypt", "cipher": "Caesar", "original": "mjqqt, btwqi!", "result": "hello, world!", "time": now},
            ],
        },
        "caesar-cipher.png": {
            "mode": "Encrypt",
            "cipher": "Caesar Cipher",
            "shift": 11,
            "input": "cipherflow",
            "output": "nryspqwlzb",
            "key": "",
            "hint": "",
            "validation": "",
            "copied": "",
            "history": [
                {"mode": "Encrypt", "cipher": "Caesar", "original": "cipherflow", "result": "nryspqwlzb", "time": now},
                {"mode": "Encrypt", "cipher": "Caesar", "original": "modern ui", "result": "xzhqry vd", "time": now},
            ],
        },
        "vigenere-cipher.png": {
            "mode": "Encrypt",
            "cipher": "Vigen\u00e8re Cipher",
            "shift": 3,
            "input": "portfolio ready",
            "output": "rsrdqowka gflim",
            "key": "CLEAN",
            "hint": "Generated alphabetic key.",
            "validation": "",
            "copied": "",
            "history": [
                {"mode": "Encrypt", "cipher": "Vigen\u00e8re", "original": "portfolio ready", "result": "rsrdqowka gflim", "time": now},
            ],
        },
        "xor-cipher.png": {
            "mode": "Decrypt",
            "cipher": "XOR Cipher",
            "shift": 3,
            "input": "Gx0nUQ==",
            "output": "note",
            "key": "A9K2X1",
            "hint": "Generated alphanumeric key.",
            "validation": "",
            "copied": "",
            "history": [
                {"mode": "Decrypt", "cipher": "XOR", "original": "Gx0nUQ==", "result": "note", "time": now},
            ],
        },
    }


def main():
    for filename, state in build_states().items():
        draw_window(state, filename)


if __name__ == "__main__":
    main()
