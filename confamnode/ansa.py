import uuid
from dataclasses import dataclass, field


@dataclass
class Usage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class Cost:
    naira: float
    naira_input: float = 0.0
    naira_output: float = 0.0
    dollars: float | None = None


@dataclass
class Ansa:
    text: str
    model: str
    usage: Usage
    cost: Cost
    finish_reason: str
    raw: object
    reasoning: str | None = None
    tools: list = field(default_factory=list)
    citations: list = field(default_factory=list)
    id: str = field(default_factory=lambda: f"confam-{uuid.uuid4()}")
    is_local: bool = False
    is_ngn_data_residency: bool = False


@dataclass
class StreamDelta:
    role: str | None = None
    content: str | None = None
    reasoning: str | None = None


@dataclass
class StreamChoice:
    index: int = 0
    delta: StreamDelta = field(default_factory=StreamDelta)
    finish_reason: str | None = None


@dataclass
class StreamChunk:
    id: str = ""
    model: str = ""
    choices: list = field(default_factory=list)