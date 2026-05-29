from __future__ import annotations


class VigenereCipher:
    @staticmethod
    def _key_shifts(key: str) -> list[int]:
        return [ord(char.lower()) - ord("a") for char in key if char.isalpha()]

    @classmethod
    def _transform(cls, text: str, key: str, decrypt: bool = False) -> str:
        shifts = cls._key_shifts(key)
        if not shifts:
            raise ValueError("Please enter a valid key")

        result: list[str] = []
        key_index = 0

        for char in text:
            if not char.isalpha():
                result.append(char)
                continue

            shift = shifts[key_index % len(shifts)]
            if decrypt:
                shift = -shift

            base = ord("A") if char.isupper() else ord("a")
            offset = (ord(char) - base + shift) % 26
            result.append(chr(base + offset))
            key_index += 1

        return "".join(result)

    @classmethod
    def encrypt(cls, text: str, key: str) -> str:
        return cls._transform(text, key, decrypt=False)

    @classmethod
    def decrypt(cls, text: str, key: str) -> str:
        return cls._transform(text, key, decrypt=True)
