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