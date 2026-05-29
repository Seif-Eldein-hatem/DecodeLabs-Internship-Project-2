from __future__ import annotations

import customtkinter as ctk

from ui.components import CardFrame
from ui.styles import ACCENT, BORDER, PRIMARY, MUTED, BODY_FONT, SMALL_FONT
from utils.history_manager import HistoryEntry


class HistoryPanel(CardFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, title="History", **kwargs)
        self.grid_rowconfigure(1, weight=1)
        self.body = ctk.CTkFrame(self, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.body.grid_columnconfigure(0, weight=1)

        self.empty_label = ctk.CTkLabel(
            self.body,
            text="No operations yet.",
            font=SMALL_FONT,
            text_color=MUTED,
            anchor="w",
        )
        self.empty_label.grid(row=0, column=0, sticky="ew")

    def refresh(self, entries: list[HistoryEntry]) -> None:
        for child in self.body.winfo_children():
            child.destroy()

        if not entries:
            self.empty_label = ctk.CTkLabel(
                self.body,
                text="No operations yet.",
                font=SMALL_FONT,
                text_color=MUTED,
                anchor="w",
            )
            self.empty_label.grid(row=0, column=0, sticky="ew")
            return

        for index, entry in enumerate(reversed(entries)):
            card = ctk.CTkFrame(
                self.body,
                fg_color="#FBFCFB",
                border_width=1,
                border_color=BORDER,
                corner_radius=12,
            )
            card.grid(row=index, column=0, sticky="ew", pady=(0, 10))
            card.grid_columnconfigure(0, weight=1)

            header = ctk.CTkLabel(
                card,
                text=f"[{entry.mode}] {entry.cipher}",
                font=BODY_FONT,
                text_color=PRIMARY,
                anchor="w",
            )
            header.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 2))

            body = ctk.CTkLabel(
                card,
                text=f"{entry.original_text} → {entry.result_text}",
                font=SMALL_FONT,
                text_color=ACCENT,
                anchor="w",
                justify="left",
                wraplength=360,
            )
            body.grid(row=1, column=0, sticky="ew", padx=12)

            timestamp = ctk.CTkLabel(
                card,
                text=entry.timestamp,
                font=SMALL_FONT,
                text_color=MUTED,
                anchor="w",
            )
            timestamp.grid(row=2, column=0, sticky="ew", padx=12, pady=(2, 10))
