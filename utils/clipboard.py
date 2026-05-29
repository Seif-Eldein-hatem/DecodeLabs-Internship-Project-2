from __future__ import annotations

from typing import Optional


def copy_text(text: str, fallback_widget: Optional[object] = None) -> None:
    try:
        import pyperclip

        pyperclip.copy(text)
        return
    except Exception:
        pass

    if fallback_widget is None:
        raise RuntimeError("Clipboard support is unavailable")

    fallback_widget.clipboard_clear()
    fallback_widget.clipboard_append(text)
    fallback_widget.update()
