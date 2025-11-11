"""AgentSpaces orchestrates autonomous agents via typed message passing."""

from __future__ import annotations

from .agent import BaseAgent
from .bus import MessageBus
from .contracts import AgentMsg, MsgType
from .logging import JsonLogger
from .memory import NamespacedMemory
from .tools import ToolRegistry, call_tool

__all__ = [
    "AgentMsg",
    "BaseAgent",
    "JsonLogger",
    "MessageBus",
    "MsgType",
    "NamespacedMemory",
    "ToolRegistry",
    "call_tool",
]

__version__ = "0.1.0"

