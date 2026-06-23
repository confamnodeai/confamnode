from confamnode.ansa import StreamChunk, StreamChoice, StreamDelta


def parse_chunk(raw: dict) -> StreamChunk:
    choices = []
    for c in raw.get("choices", []):
        d = c.get("delta", {})
        choices.append(StreamChoice(
            index=c.get("index", 0),
            finish_reason=c.get("finish_reason"),
            delta=StreamDelta(
                role=d.get("role"),
                content=d.get("content"),
                reasoning=d.get("reasoning")
            )
        ))
    return StreamChunk(
        id=raw.get("id", ""),
        model=raw.get("model", ""),
        choices=choices,
    )