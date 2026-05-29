from __future__ import annotations


def validate_caesar_shift(value: int) -> None:
    if not 0 <= int(value) <= 25:
        raise ValueError("Please enter a valid key")


def validate_vigenere_key(key: str) -> None:
    if not key or not key.isalpha():
        raise ValueError("Please enter a valid key")


def validate_xor_key(key: str) -> None:
    if not key.strip():
        raise ValueError("Please enter a valid key")
