from __future__ import annotations

import customtkinter as ctk


BACKGROUND = "#F5F5F5"
PRIMARY = "#1E2A38"
ACCENT = "#A3B18A"
TEXT = "#222222"
CARD = "#FFFFFF"
BORDER = "#D9D9D9"
MUTED = "#6C7075"
ERROR = "#B85C5C"


def configure_theme() -> None:
    ctk.set_appearance_mode("Light")
    try:
        ctk.set_default_color_theme("blue")
    except Exception:  # noqa: BLE001
        pass


def font(size: int, weight: str = "normal") -> tuple[str, int, str]:
    return ("Segoe UI", size, weight)


TITLE_FONT = font(30, "bold")
SUBTITLE_FONT = font(14, "normal")
SECTION_FONT = font(16, "bold")
BODY_FONT = font(13, "normal")
BODY_MEDIUM = font(13, "bold")
SMALL_FONT = font(11, "normal")
