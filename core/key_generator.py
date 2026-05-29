from __future__ import annotations

import random
import string


class KeyGenerator:
    @staticmethod
    def caesar() -> int:
        return random.randint(1, 25)

    @staticmethod
    def vigenere(length: int = 5) -> str:
        length = max(3, length)
        return "".join(random.choice(string.ascii_uppercase) for _ in range(length))

    @staticmethod
    def xor(length: int = 6) -> str:
        length = max(4, length)
        alphabet = string.ascii_uppercase + string.digits
        return "".join(random.choice(alphabet) for _ in range(length))
