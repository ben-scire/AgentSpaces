"""Minimal JSON structured logger."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Dict


class JsonLogger:
    """Outputs structured log entries to stdout."""

    def __init__(self, *, service: str = "agentspaces") -> None:
        self.service = service

    def info(self, event: str, **fields: Any) -> None:
        """Emit an informational event with optional structured fields."""

        self._emit("info", event, fields)

    def error(self, event: str, **fields: Any) -> None:
        """Emit an error event with optional structured fields."""

        self._emit("error", event, fields)

    def _emit(self, level: str, event: str, fields: Dict[str, Any]) -> None:
        record = {
            "ts": datetime.now(tz=timezone.utc).isoformat(),
            "level": level,
            "service": self.service,
            "event": event,
            **fields,
        }
        print(json.dumps(record, sort_keys=True))

