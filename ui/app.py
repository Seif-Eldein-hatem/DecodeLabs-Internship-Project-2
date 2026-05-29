from __future__ import annotations

import customtkinter as ctk

from core.caesar_cipher import CaesarCipher
from core.key_generator import KeyGenerator
from core.vigenere_cipher import VigenereCipher
from core.xor_cipher import XORCipher
from ui.components import CardFrame, GhostButton, HintLabel, InputBox, ReadOnlyBox, RoundedButton, SectionLabel
from ui.history_panel import HistoryPanel
from ui.styles import ACCENT, BACKGROUND, BORDER, ERROR, MUTED, PRIMARY, TEXT, configure_theme, font, BODY_FONT, BODY_MEDIUM, SMALL_FONT, TITLE_FONT, SUBTITLE_FONT
from utils.clipboard import copy_text
from utils.history_manager import HistoryManager
from utils.validators import validate_vigenere_key, validate_xor_key


class CipherFlowApp(ctk.CTk):
    def __init__(self) -> None:
        configure_theme()
        super().__init__()

        self.title("CipherFlow")
        self.configure(fg_color=BACKGROUND)
        self.geometry("1360x920")
        self.minsize(1200, 860)

        self.history_manager = HistoryManager()
        self.history_entries = self.history_manager.load()
        self._pending_update: str | None = None
        self._last_signature: tuple[str, str, str, str, str] | None = None
        self._copy_reset_job: str | None = None

        self.mode_var = ctk.StringVar(value="Encrypt")
        self.cipher_var = ctk.StringVar(value="Caesar Cipher")
        self.key_var = ctk.StringVar(value="")
        self.caesar_var = ctk.IntVar(value=3)
        self.output_text = ""

        self._build_layout()
        self._bind_traces()
        self.refresh_dynamic_controls()
        self.schedule_update()
        self.history_panel.refresh(self.history_entries)
        self.after(0, self._maximize_on_start)

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1, uniform="layout")
        self.grid_columnconfigure(1, weight=1, uniform="layout")
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=28, pady=(24, 12))
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(header, text="CipherFlow", font=TITLE_FONT, text_color=PRIMARY, anchor="w")
        title.grid(row=0, column=0, sticky="ew")

        subtitle = ctk.CTkLabel(
            header,
            text="Real-time text encryption utility",
            font=SUBTITLE_FONT,
            text_color=MUTED,
            anchor="w",
        )
        subtitle.grid(row=1, column=0, sticky="ew", pady=(2, 0))

        self.left_card = CardFrame(self, title="Controls")
        self.left_card.grid(row=1, column=0, sticky="nsew", padx=(28, 14), pady=(0, 24))
        self.left_card.grid_columnconfigure(0, weight=1)
        self.left_card.grid_rowconfigure(3, weight=1)

        self.right_card = CardFrame(self, title="Output")
        self.right_card.grid(row=1, column=1, sticky="nsew", padx=(14, 28), pady=(0, 24))
        self.right_card.grid_columnconfigure(0, weight=1)
        self.right_card.grid_rowconfigure(3, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    def _build_left_panel(self) -> None:
        self.left_body = ctk.CTkFrame(self.left_card, fg_color="transparent")
        self.left_body.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.left_body.grid_columnconfigure(0, weight=1)

        SectionLabel(self.left_body, "Mode").grid(row=0, column=0, sticky="ew")
        self.mode_selector = ctk.CTkSegmentedButton(
            self.left_body,
            values=["Encrypt", "Decrypt"],
            command=self._on_mode_change,
            fg_color="#E7EAE7",
            selected_color=PRIMARY,
            selected_hover_color="#304251",
            unselected_color="#E7EAE7",
            unselected_hover_color="#DDE2DD",
            text_color=PRIMARY,
            text_color_disabled=MUTED,
            corner_radius=12,
            font=BODY_MEDIUM,
            height=38,
        )
        self.mode_selector.set("Encrypt")
        self.mode_selector.grid(row=1, column=0, sticky="ew", pady=(8, 18))

        SectionLabel(self.left_body, "Input Text").grid(row=2, column=0, sticky="ew")
        self.input_box = InputBox(self.left_body, height=170)
        self.input_box.grid(row=3, column=0, sticky="nsew", pady=(8, 18))
        self.input_box.bind("<KeyRelease>", self._on_text_change)
        self.input_box.bind("<<Paste>>", self._on_text_change)

        SectionLabel(self.left_body, "Cipher").grid(row=4, column=0, sticky="ew")
        self.cipher_menu = ctk.CTkOptionMenu(
            self.left_body,
            values=["Caesar Cipher", "Vigen\u00e8re Cipher", "XOR Cipher"],
            variable=self.cipher_var,
            command=self._on_cipher_change,
            fg_color="#EEF1EF",
            button_color=PRIMARY,
            button_hover_color=ACCENT,
            text_color=PRIMARY,
            dropdown_fg_color="white",
            dropdown_text_color=TEXT,
            dropdown_hover_color="#EFF3EF",
            font=BODY_MEDIUM,
            height=38,
            corner_radius=12,
        )
        self.cipher_menu.grid(row=5, column=0, sticky="ew", pady=(8, 18))

        self.controls_frame = ctk.CTkFrame(self.left_body, fg_color="transparent")
        self.controls_frame.grid(row=6, column=0, sticky="ew")
        self.controls_frame.grid_columnconfigure(0, weight=1)

        self.caesar_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.caesar_frame.grid_columnconfigure(0, weight=1)

        self.caesar_label = SectionLabel(self.caesar_frame, "Caesar Shift")
        self.caesar_label.grid(row=0, column=0, sticky="ew")

        slider_row = ctk.CTkFrame(self.caesar_frame, fg_color="transparent")
        slider_row.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        slider_row.grid_columnconfigure(0, weight=1)

        self.caesar_slider = ctk.CTkSlider(
            slider_row,
            from_=0,
            to=25,
            number_of_steps=25,
            command=self._on_slider_change,
            progress_color=ACCENT,
            button_color=PRIMARY,
            button_hover_color="#304251",
        )
        self.caesar_slider.set(self.caesar_var.get())
        self.caesar_slider.grid(row=0, column=0, sticky="ew")

        self.caesar_value_label = HintLabel(slider_row, f"Shift: {self.caesar_var.get()}", color=PRIMARY)
        self.caesar_value_label.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.key_frame = ctk.CTkFrame(self.controls_frame, fg_color="transparent")
        self.key_frame.grid_columnconfigure(0, weight=1)

        self.key_label = SectionLabel(self.key_frame, "Key")
        self.key_label.grid(row=0, column=0, sticky="ew")

        self.key_entry = ctk.CTkEntry(
            self.key_frame,
            textvariable=self.key_var,
            fg_color="white",
            border_color=BORDER,
            corner_radius=12,
            height=38,
            font=BODY_FONT,
        )
        self.key_entry.grid(row=1, column=0, sticky="ew", pady=(8, 0))

        self.key_hint = HintLabel(self.key_frame, "", color=MUTED)
        self.key_hint.grid(row=2, column=0, sticky="ew", pady=(6, 0))

        self.generate_button = RoundedButton(self.left_body, text="Generate Key", command=self.generate_key)
        self.generate_button.grid(row=7, column=0, sticky="ew", pady=(18, 10))

        self.validation_label = HintLabel(self.left_body, "", color=ERROR)
        self.validation_label.grid(row=8, column=0, sticky="ew")

    def _build_right_panel(self) -> None:
        self.right_body = ctk.CTkFrame(self.right_card, fg_color="transparent")
        self.right_body.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.right_body.grid_columnconfigure(0, weight=1)
        self.right_body.grid_rowconfigure(1, weight=1)
        self.right_body.grid_rowconfigure(3, weight=1)

        SectionLabel(self.right_body, "Live Output").grid(row=0, column=0, sticky="ew")
        self.output_box = ReadOnlyBox(self.right_body, height=170)
        self.output_box.grid(row=1, column=0, sticky="nsew", pady=(8, 14))

        actions = ctk.CTkFrame(self.right_body, fg_color="transparent")
        actions.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)

        self.copy_button = GhostButton(actions, text="Copy Output", command=self.copy_output)
        self.copy_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))

        self.clear_button = GhostButton(actions, text="Clear All", command=self.clear_all)
        self.clear_button.grid(row=0, column=1, sticky="ew", padx=(8, 0))

        self.copy_feedback = HintLabel(self.right_body, "", color=ACCENT)
        self.copy_feedback.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        self.history_panel = HistoryPanel(self.right_body)
        self.history_panel.grid(row=4, column=0, sticky="nsew")

    def _maximize_on_start(self) -> None:
        try:
            self.state("zoomed")
        except Exception:
            try:
                self.attributes("-zoomed", True)
            except Exception:
                pass

    def _bind_traces(self) -> None:
        self.key_var.trace_add("write", lambda *_: self.schedule_update())
        self.cipher_var.trace_add("write", lambda *_: self.schedule_update())
        self.caesar_var.trace_add("write", lambda *_: self.schedule_update())

    def _on_text_change(self, _event=None) -> None:
        self.schedule_update()

    def _on_mode_change(self, value: str) -> None:
        self.mode_var.set(value)
        self.schedule_update()

    def _on_cipher_change(self, value: str) -> None:
        self.cipher_var.set(value)
        self.refresh_dynamic_controls()
        self.schedule_update()

    def _on_slider_change(self, value: float) -> None:
        shift = int(round(value))
        self.caesar_var.set(shift)
        self.caesar_value_label.configure(text=f"Shift: {shift}")

    def refresh_dynamic_controls(self) -> None:
        self.caesar_frame.grid_remove()
        self.key_frame.grid_remove()

        cipher = self.cipher_var.get()
        self.key_hint.configure(text="")

        if cipher == "Caesar Cipher":
            self.caesar_frame.grid(row=0, column=0, sticky="ew")
            self.generate_button.configure(text="Generate Key")
        else:
            self.key_frame.grid(row=0, column=0, sticky="ew")
            self.generate_button.configure(text="Generate Key")

    def schedule_update(self) -> None:
        if self._pending_update is not None:
            self.after_cancel(self._pending_update)
        self._pending_update = self.after(90, self.update_output)

    def get_input_text(self) -> str:
        return self.input_box.get_text()

    def set_output_text(self, text: str) -> None:
        self.output_text = text
        self.output_box.set_text(text)

    def update_output(self) -> None:
        self._pending_update = None
        original = self.get_input_text()
        cipher = self.cipher_var.get()
        mode = self.mode_var.get()
        key = self.key_var.get().strip()
        shift = int(self.caesar_var.get())

        self.validation_label.configure(text="")

        if not original:
            self.set_output_text("")
            return

        try:
            if cipher == "Caesar Cipher":
                if mode == "Encrypt":
                    result = CaesarCipher.encrypt(original, shift)
                else:
                    result = CaesarCipher.decrypt(original, shift)
            elif cipher == "Vigen\u00e8re Cipher":
                validate_vigenere_key(key)
                if mode == "Encrypt":
                    result = VigenereCipher.encrypt(original, key)
                else:
                    result = VigenereCipher.decrypt(original, key)
            else:
                validate_xor_key(key)
                if mode == "Encrypt":
                    result = XORCipher.encrypt(original, key)
                else:
                    result = XORCipher.decrypt(original, key)
        except ValueError as exc:
            self.validation_label.configure(text=str(exc), text_color=ERROR)
            self.set_output_text("")
            return

        self.set_output_text(result)
        signature = (mode, cipher, original, result, key if cipher != "Caesar Cipher" else str(shift))
        if signature != self._last_signature:
            self._last_signature = signature
            self.history_entries = self.history_manager.append(
                self.history_entries,
                mode=mode,
                cipher=cipher,
                original_text=original,
                result_text=result,
            )
            self.history_panel.refresh(self.history_entries)

    def generate_key(self) -> None:
        cipher = self.cipher_var.get()
        if cipher == "Caesar Cipher":
            self.caesar_var.set(KeyGenerator.caesar())
            self.caesar_slider.set(self.caesar_var.get())
            self.caesar_value_label.configure(text=f"Shift: {self.caesar_var.get()}")
        elif cipher == "Vigen\u00e8re Cipher":
            key = KeyGenerator.vigenere()
            self.key_var.set(key)
            self.key_hint.configure(text="Generated alphabetic key.", text_color=ACCENT)
        else:
            key = KeyGenerator.xor()
            self.key_var.set(key)
            self.key_hint.configure(text="Generated alphanumeric key.", text_color=ACCENT)

        self.schedule_update()

    def copy_output(self) -> None:
        text = self.output_text.strip()
        if not text:
            self.copy_feedback.configure(text="Nothing to copy.", text_color=ERROR)
            return

        try:
            copy_text(text, self)
        except Exception:
            self.copy_feedback.configure(text="Copy failed.", text_color=ERROR)
            return

        self.copy_feedback.configure(text="Copied!", text_color=ACCENT)
        if self._copy_reset_job is not None:
            self.after_cancel(self._copy_reset_job)
        self._copy_reset_job = self.after(1500, self._clear_copy_feedback)

    def _clear_copy_feedback(self) -> None:
        self._copy_reset_job = None
        self.copy_feedback.configure(text="")

    def clear_all(self) -> None:
        self.input_box.clear()
        self.output_box.set_text("")
        self.output_text = ""
        self.key_var.set("")
        self.caesar_var.set(0)
        self.caesar_slider.set(0)
        self.caesar_value_label.configure(text="Shift: 0")
        self.validation_label.configure(text="")
        self.key_hint.configure(text="")
        self.copy_feedback.configure(text="")
        self._last_signature = None
        self.schedule_update()
