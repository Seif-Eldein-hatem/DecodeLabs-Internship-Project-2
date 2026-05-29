from __future__ import annotations

import customtkinter as ctk

from ui.styles import ACCENT, BORDER, CARD, ERROR, PRIMARY, TEXT, BODY_FONT, BODY_MEDIUM, SECTION_FONT, SMALL_FONT


class CardFrame(ctk.CTkFrame):
    def __init__(self, master, *, title: str | None = None, **kwargs):
        super().__init__(
            master,
            fg_color=CARD,
            border_width=1,
            border_color=BORDER,
            corner_radius=18,
            **kwargs,
        )
        self.grid_columnconfigure(0, weight=1)
        if title:
            self.title_label = ctk.CTkLabel(
                self,
                text=title,
                font=SECTION_FONT,
                text_color=PRIMARY,
                anchor="w",
            )
            self.title_label.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))


class SectionLabel(ctk.CTkLabel):
    def __init__(self, master, text: str, **kwargs):
        super().__init__(master, text=text, font=BODY_MEDIUM, text_color=PRIMARY, anchor="w", **kwargs)


class HintLabel(ctk.CTkLabel):
    def __init__(self, master, text: str = "", *, color: str = TEXT, **kwargs):
        super().__init__(master, text=text, font=SMALL_FONT, text_color=color, anchor="w", **kwargs)
        self._default_color = color

    def set(self, text: str, *, color: str | None = None) -> None:
        self.configure(text=text, text_color=color or self._default_color)


class RoundedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=PRIMARY,
            hover_color=ACCENT,
            text_color="white",
            corner_radius=12,
            font=BODY_MEDIUM,
            height=38,
            **kwargs,
        )


class GhostButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="#EEF1EF",
            hover_color="#E4E8E4",
            text_color=PRIMARY,
            corner_radius=12,
            font=BODY_MEDIUM,
            height=38,
            **kwargs,
        )


class ReadOnlyBox(ctk.CTkTextbox):
    def __init__(self, master, *, height: int = 160, **kwargs):
        super().__init__(
            master,
            height=height,
            fg_color="#FAFAFA",
            text_color=TEXT,
            border_width=1,
            border_color=BORDER,
            corner_radius=14,
            wrap="word",
            font=BODY_FONT,
            **kwargs,
        )
        self.configure(state="disabled")

    def set_text(self, text: str) -> None:
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert("1.0", text)
        self.configure(state="disabled")

    def get_text(self) -> str:
        return self.get("1.0", "end-1c")


class InputBox(ctk.CTkTextbox):
    def __init__(self, master, *, height: int = 220, **kwargs):
        super().__init__(
            master,
            height=height,
            fg_color="white",
            text_color=TEXT,
            border_width=1,
            border_color=BORDER,
            corner_radius=14,
            wrap="word",
            font=BODY_FONT,
            **kwargs,
        )

    def clear(self) -> None:
        self.delete("1.0", "end")

    def get_text(self) -> str:
        return self.get("1.0", "end-1c")

    def set_text(self, text: str) -> None:
        self.delete("1.0", "end")
        self.insert("1.0", text)
