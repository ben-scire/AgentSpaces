# Inspired by message-passing patterns used in Icarus AgentSpaces communication workflow
"""In-process pub/sub message bus."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, MutableMapping

from .agent import BaseAgent
from .contracts import AgentMsg
from .logging import JsonLogger


class MessageBus:
    """Synchronously routes messages between agents subscribed to topics."""

    def __init__(self, logger: JsonLogger | None = None) -> None:
        self._subscriptions: MutableMapping[str, List[BaseAgent]] = defaultdict(list)
        self._logger = logger or JsonLogger()

    @property
    def topics(self) -> Iterable[str]:
        """Return currently registered topics."""

        return tuple(self._subscriptions.keys())

    def register(self, agent: BaseAgent) -> None:
        """Subscribe an agent to its declared topics."""

        for topic in agent.subscriptions():
            self.subscribe(topic, agent)

    def subscribe(self, topic: str, agent: BaseAgent) -> None:
        """Attach an agent to a topic."""

        if agent not in self._subscriptions[topic]:
            self._subscriptions[topic].append(agent)
            self._logger.info("subscribed", topic=topic, agent=agent.name)

    def publish(self, message: AgentMsg) -> None:
        """Deliver a message to all agents subscribed to its target."""

        self._logger.info(
            "publish",
            target=message.target,
            msg_type=message.type.value,
            source=message.source,
            trace_id=message.trace_id,
            parent_id=message.parent_id,
        )
        for agent in list(self._subscriptions.get(message.target, [])):
            agent.handle(message, self)

