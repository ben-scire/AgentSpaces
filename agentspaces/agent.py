"""Abstract agent contract."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Tuple

from .contracts import AgentMsg

if TYPE_CHECKING:
    from .bus import MessageBus


class BaseAgent(ABC):
    """Shared behavior for all agents."""

    def __init__(self, name: str | None = None) -> None:
        self._name = name or self.__class__.__name__

    @property
    def name(self) -> str:
        """Human-readable identifier for logging and routing."""

        return self._name

    def subscriptions(self) -> Tuple[str, ...]:
        """Topics this agent wants to receive; override as needed."""

        return ()

    @abstractmethod
    def handle(self, message: AgentMsg, bus: "MessageBus") -> None:
        """React to an incoming message and optionally publish via the bus."""

        raise NotImplementedError

