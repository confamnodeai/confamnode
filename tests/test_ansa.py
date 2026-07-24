from confamnode.ansa import (
    Ansa, 
    Cost,
    Usage,
    EmbeddingUsage,
    EmbeddingResult,
)


def test_usage_has_prompt_tokens():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    assert usage.prompt_tokens == 10


def test_usage_has_completion_tokens():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    assert usage.completion_tokens == 20


def test_usage_has_total_tokens():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    assert usage.total_tokens == 30


def test_cost_has_naira():
    cost = Cost(naira=1.23)
    assert cost.naira == 1.23


def test_cost_dollars_is_none_by_default():
    cost = Cost(naira=1.23)
    assert cost.dollars is None


def test_cost_accepts_dollars():
    cost = Cost(naira=1.23, dollars=0.0008)
    assert cost.dollars == 0.0008


def test_ansa_has_text():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.text == "How far!"


def test_ansa_has_model():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.model == "confam-speed"


def test_ansa_reasoning_is_none_by_default():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.reasoning is None


def test_ansa_tools_is_empty_list_by_default():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.tools == []


def test_ansa_has_usage():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.usage.total_tokens == 30


def test_ansa_has_finish_reason():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.finish_reason == "stop"


def test_ansa_has_raw():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    raw = {"id": "abc123"}
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw=raw
    )
    assert ansa.raw == {"id": "abc123"}


def test_ansa_accepts_reasoning():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="The answer is 42",
        model="confam-reasoning",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
        reasoning="First I thought about it..."
    )
    assert ansa.reasoning == "First I thought about it..."


def test_ansa_accepts_tools():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="",
        model="confam-agents",
        usage=usage,
        cost=cost,
        finish_reason="tool_calls",
        raw={},
        tools=[{"name": "search", "arguments": {"query": "Lagos weather"}}]
    )
    assert len(ansa.tools) == 1
    assert ansa.tools[0]["name"] == "search"


def test_ansa_has_id():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
    )
    assert ansa.id.startswith("confam-")


def test_ansa_id_is_unique():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa1 = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
    )
    ansa2 = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
    )
    assert ansa1.id != ansa2.id


def test_ansa_citations_is_empty_list_by_default():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.citations == []


def test_ansa_accepts_citations():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="Nigerian GDP grew by 3.4%",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
        citations=[
            {"source": "World Bank", "url": "https://worldbank.org/"},
            {"source": "NBS Nigeria", "url": "https://nigerianstat.gov.ng/"}
        ]
    )
    assert len(ansa.citations) == 2
    assert ansa.citations[0]["source"] == "World Bank"


def test_ansa_is_local_defaults_to_false():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.is_local == False


def test_ansa_is_ngn_data_residency_resident_defaults_to_false():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={}
    )
    assert ansa.is_ngn_data_residency == False


def test_ansa_accepts_is_local_true():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How far!",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={},
        is_local=True,
        is_ngn_data_residency=True
    )
    assert ansa.is_local == True
    assert ansa.is_ngn_data_residency == True


def test_ansa_raw_is_dict():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How you dey?",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw={
            "id": "confam-resp-abc123",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
            }
        }
    )
    assert isinstance(ansa.raw, dict)


def test_ansa_raw_does_not_expose_model_routing():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    raw = {
        "id": "confam-resp-abc123",
        "finish_reason": "stop",
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
        }
    }
    ansa = Ansa(
        text="How you dey?",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw=raw
    )
    assert "model" not in ansa.raw
    assert "openai" not in str(ansa.raw)
    assert "_hidden_params" not in ansa.raw


def test_ansa_raw_has_id():
    usage = Usage(prompt_tokens=10, completion_tokens=20, total_tokens=30)
    cost = Cost(naira=1.23)
    ansa = Ansa(
        text="How you dey?",
        model="confam-speed",
        usage=usage,
        cost=cost,
        finish_reason="stop",
        raw = {"id": "confam-resp-abc123", "finish_reason": "stop", "usage": {}}
    )
    assert ansa.raw["id"] == "confam-resp-abc123"


def test_embedding_usage_has_prompt_tokens():
    usage = EmbeddingUsage(prompt_tokens=15, total_tokens=15)
    assert usage.prompt_tokens == 15


def test_embedding_usage_has_total_tokens():
    usage = EmbeddingUsage(prompt_tokens=15, total_tokens=15)
    assert usage.total_tokens == 15


def test_embedding_usage_has_no_completion_tokens_field():
    # Embeddings have no output tokens to bill -- deliberately no
    # completion_tokens field, unlike chat Usage.
    usage = EmbeddingUsage(prompt_tokens=15, total_tokens=15)
    assert not hasattr(usage, "completion_tokens")


def test_embedding_result_has_embeddings():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1, 0.2, 0.3],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert result.embeddings == [0.1, 0.2, 0.3]


def test_embedding_result_has_model():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1, 0.2],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert result.model == "confam-embed-local"


def test_embedding_result_has_id():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1, 0.2],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert result.id.startswith("confam-")


def test_embedding_result_is_local_defaults_to_false():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1],
        model="confam-embed-text-1",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert result.is_local is False
    assert result.is_ngn_data_residency is False


def test_embedding_result_accepts_is_local_true():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={},
        is_local=True,
        is_ngn_data_residency=True
    )
    assert result.is_local is True
    assert result.is_ngn_data_residency is True


def test_embedding_result_task_type_applied_defaults_to_none():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1],
        model="confam-embed-text-1",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert result.task_type_applied is None


def test_embedding_result_accepts_task_type_applied():
    usage = EmbeddingUsage(prompt_tokens=5, total_tokens=5)
    cost = Cost(naira=0.5)
    result = EmbeddingResult(
        embeddings=[0.1],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={},
        task_type_applied="document"
    )
    assert result.task_type_applied == "document"


def test_embedding_result_handles_list_of_vectors():
    # A multi-input embed() call returns a list of vectors, not one --
    # this is the shape when the caller passed a list, not a string.
    usage = EmbeddingUsage(prompt_tokens=10, total_tokens=10)
    cost = Cost(naira=1.0)
    result = EmbeddingResult(
        embeddings=[[0.1, 0.2], [0.3, 0.4]],
        model="confam-embed-local",
        usage=usage,
        cost=cost,
        raw={}
    )
    assert len(result.embeddings) == 2
    assert result.embeddings[0] == [0.1, 0.2]