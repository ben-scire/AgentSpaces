"""Core message contracts used across AgentSpaces."""

from __future__ import annotations

import time
import uuid
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field


class MsgType(str, Enum):
    """Enumerates the intent of a message."""

    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"


class AgentMsg(BaseModel):
    """Typed payload exchanged between agents via the message bus."""

    model_config = ConfigDict(frozen=True)

    type: MsgType = Field(..., description="Semantic intent of the message.")
    source: str = Field(..., description="Agent emitting the message.")
    target: str = Field(..., description="Topic or agent name to receive the message.")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Structured body.")
    trace_id: str = Field(default_factory=lambda: uuid.uuid4().hex, description="Trace identifier.")
    parent_id: Optional[str] = Field(
        default=None, description="Trace identifier of the upstream message."
    )
    ts: float = Field(default_factory=lambda: time.time(), description="Epoch timestamp in seconds.")


