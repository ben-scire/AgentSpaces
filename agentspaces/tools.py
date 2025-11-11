"""Tool allowlisting for controlled agent execution."""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable


Tool = Callable[..., Any]


class ToolRegistry:
    """Maintain a mapping of permitted tool callables keyed by name."""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def allow(self, name: str, func: Tool) -> None:
        """Register or replace an allowed tool."""

        self._tools[name] = func

    def revoke(self, name: str) -> None:
        """Remove a tool from the allowlist."""

        self._tools.pop(name, None)

    def names(self) -> Iterable[str]:
        """Return the currently allowed tool names."""

        return tuple(self._tools.keys())

    def call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        """Invoke an allowed tool, raising ``KeyError`` when missing."""

        if name not in self._tools:
            raise KeyError(f"tool '{name}' is not allowed")
        return self._tools[name](*args, **kwargs)


def call_tool(registry: ToolRegistry, name: str, *args: Any, **kwargs: Any) -> Any:
    """Convenience helper that proxies to ``ToolRegistry.call``."""

    return registry.call(name, *args, **kwargs)

