"""Example pipeline demonstrating an echo interaction."""

from __future__ import annotations

from typing import Any

from agentspaces.agent import BaseAgent
from agentspaces.bus import MessageBus
from agentspaces.contracts import AgentMsg, MsgType
from agentspaces.logging import JsonLogger
from agentspaces.memory import NamespacedMemory


class EchoAgent(BaseAgent):
    """Echoes incoming messages and tracks invocation count."""

    def __init__(self, memory: NamespacedMemory) -> None:
        super().__init__(name="EchoAgent")
        self._memory = memory

    def subscriptions(self) -> tuple[str, ...]:
        return ("echo",)

    def handle(self, message: AgentMsg, bus: MessageBus) -> None:
        text = str(message.payload.get("text", ""))
        count = int(self._memory.get("echo", "count", 0)) + 1
        self._memory.set("echo", "count", count)
        response = AgentMsg(
            type=MsgType.RESPONSE,
            source=self.name,
            target="sink",
            payload={"text": text, "count": count},
            parent_id=message.trace_id,
        )
        bus.publish(response)


class SinkAgent(BaseAgent):
    """Terminal consumer that prints received payloads."""

    def __init__(self, logger: JsonLogger) -> None:
        super().__init__(name="SinkAgent")
        self._logger = logger

    def subscriptions(self) -> tuple[str, ...]:
        return ("sink",)

    def handle(self, message: AgentMsg, bus: MessageBus) -> None:  # noqa: D401
        payload: dict[str, Any] = dict(message.payload)
        text = payload.get("text", "")
        count = payload.get("count", 0)
        statement = f"EchoAgent responded '{text}' (count={count})."
        print(statement)
        self._logger.info(
            "sink_received",
            source=message.source,
            target=message.target,
            msg_type=message.type.value,
            text=text,
            count=count,
        )


def main() -> None:
    """Run the echo pipeline end-to-end."""

    logger = JsonLogger(service="agentspaces-demo")
    memory = NamespacedMemory()
    bus = MessageBus(logger=logger)

    echo_agent = EchoAgent(memory)
    sink_agent = SinkAgent(logger)

    bus.register(echo_agent)
    bus.register(sink_agent)

    message = AgentMsg(
        type=MsgType.REQUEST,
        source="cli",
        target="echo",
        payload={"text": "Hello, AgentSpaces!"},
    )

    bus.publish(message)


if __name__ == "__main__":
    main()

