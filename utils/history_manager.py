from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "history.json"


@dataclass(slots=True)
class HistoryEntry:
    mode: str
    cipher: str
    original_text: str
    result_text: str
    timestamp: str


class HistoryManager:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DATA_FILE
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[HistoryEntry]:
        if not self.path.exists():
            self.save([])
            return []

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

        entries: list[HistoryEntry] = []
        for item in raw if isinstance(raw, list) else []:
            try:
                entries.append(
                    HistoryEntry(
                        mode=str(item["mode"]),
                        cipher=str(item["cipher"]),
                        original_text=str(item["original_text"]),
                        result_text=str(item["result_text"]),
                        timestamp=str(item["timestamp"]),
                    )
                )
            except Exception:  # noqa: BLE001
                continue
        return entries

    def save(self, entries: list[HistoryEntry]) -> None:
        payload = [asdict(entry) for entry in entries[-5:]]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def append(
        self,
        entries: list[HistoryEntry],
        *,
        mode: str,
        cipher: str,
        original_text: str,
        result_text: str,
    ) -> list[HistoryEntry]:
        new_entry = HistoryEntry(
            mode=mode,
            cipher=cipher,
            original_text=original_text,
            result_text=result_text,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        updated = (entries + [new_entry])[-5:]
        self.save(updated)
        return updated
