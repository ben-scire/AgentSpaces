import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)  # keep CI quiet

from agentspaces.bus import MessageBus
from agentspaces.memory import NamespacedMemory
from agentspaces.logging import JsonLogger
from agentspaces.contracts import AgentMsg, MsgType
from agentspaces.examples.echo_pipeline import EchoAgent, SinkAgent


def test_pipeline_runs(capsys):
    """
    Sanity test: EchoAgent should receive a REQUEST on topic='echo',
    bump an invocation counter in NamespacedMemory, and emit a RESPONSE
    to topic='sink' that SinkAgent prints.
    """
    logger = JsonLogger(service="agentspaces-test")
    memory = NamespacedMemory()
    bus = MessageBus(logger=logger)

    echo = EchoAgent(memory)
    sink = SinkAgent(logger)

    # Wire agents using the framework's register() API
    bus.register(echo)
    bus.register(sink)

    # Send a single message through the pipeline
    msg = AgentMsg(
        type=MsgType.REQUEST,
        source="test",
        target="echo",
        payload={"text": "hi"},
    )
    bus.publish(msg)

    # SinkAgent prints a human-readable line; capture and assert it
    out = capsys.readouterr().out.strip()
    assert "EchoAgent responded 'hi' (count=1)." in out

    # The EchoAgent also increments a namespaced counter in memory
    assert memory.get("echo", "count", 0) == 1
