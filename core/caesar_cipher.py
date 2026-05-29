from __future__ import annotations


class CaesarCipher:
    @staticmethod
    def _shift_char(char: str, shift: int) -> str:
        if not char.isalpha():
            return char

        base = ord("A") if char.isupper() else ord("a")
        offset = (ord(char) - base + shift) % 26
        return chr(base + offset)

    @classmethod
    def encrypt(cls, text: str, shift: int) -> str:
        shift %= 26
        return "".join(cls._shift_char(char, shift) for char in text)

    @classmethod
    def decrypt(cls, text: str, shift: int) -> str:
        shift %= 26
        return "".join(cls._shift_char(char, -shift) for char in text)
