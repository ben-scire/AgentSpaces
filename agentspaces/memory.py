"""Lightweight namespaced in-memory key-value store."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, MutableMapping, Optional


class NamespacedMemory:
    """Stores values by namespace and key for agent state tracking."""

    def __init__(self) -> None:
        self._store: MutableMapping[str, Dict[str, Any]] = defaultdict(dict)

    def get(self, namespace: str, key: str, default: Any | None = None) -> Any | None:
        """Retrieve a value, returning ``default`` if it is missing."""

        return self._store.get(namespace, {}).get(key, default)

    def set(self, namespace: str, key: str, value: Any) -> None:
        """Persist a value under ``namespace`` and ``key``."""

        self._store[namespace][key] = value

    def delete(self, namespace: str, key: str) -> None:
        """Remove a value if present."""

        if key in self._store.get(namespace, {}):
            del self._store[namespace][key]

    def namespaced_view(self, namespace: str) -> Dict[str, Any]:
        """Return a shallow copy of all values stored under a namespace."""

        return dict(self._store.get(namespace, {}))

    def clear(self, namespace: Optional[str] = None) -> None:
        """Clear a namespace or the entire store."""

        if namespace is None:
            self._store.clear()
        else:
            self._store.pop(namespace, None)

