from __future__ import annotations

import base64


class XORCipher:
    @staticmethod
    def _xor_bytes(data: bytes, key: bytes) -> bytes:
        if not key:
            raise ValueError("Please enter a valid key")
        return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(data))

    @classmethod
    def encrypt(cls, text: str, key: str) -> str:
        if not key:
            raise ValueError("Please enter a valid key")
        encrypted = cls._xor_bytes(text.encode("utf-8"), key.encode("utf-8"))
        return base64.b64encode(encrypted).decode("ascii")

    @classmethod
    def decrypt(cls, text: str, key: str) -> str:
        if not key:
            raise ValueError("Please enter a valid key")
        try:
            payload = base64.b64decode(text.encode("ascii"), validate=True)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("Please enter valid Base64 text") from exc
        decrypted = cls._xor_bytes(payload, key.encode("utf-8"))
        return decrypted.decode("utf-8", errors="replace")
