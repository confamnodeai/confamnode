# ConfamNode

The Nigerian AI inference gateway. Access frontier AI models.

---

## Installation

### Using pip
```bash
pip install confamnode
```

### Using uv
```bash
uv add confamnode
```

### Using virtualenv
```bash
# Create virtual environment
python -m venv venv

# Activate — Linux/Mac
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate

# Install
pip install confamnode
```

### Using uv with virtual environment
```bash
# Create project
uv init my-project
cd my-project

# Add confamnode
uv add confamnode

# Run your script
uv run python main.py
```

### Using conda
```bash
# Create environment
conda create -n my-project python=3.10
conda activate my-project

# Install
pip install confamnode
```

---

## Quick Start

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-xxx")

ansa = client.gist(
    model="gemini/gemini-3.5-flash-lite",
    messages="How you dey?"
)

print(ansa.text)
print(f"Cost: ₦{ansa.cost.naira:.6f}")
print(f"Tokens: {ansa.usage.total_tokens}")
print(f"ID: {ansa.id}")
```

---

## Streaming

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-xxx")

stream = client.gist(
    model="gemini/gemini-3.5-flash-lite",
    messages="Wetin be the capital of 9ja?",
    stream=True
)

# Print tokens as they arrive
for yarn in stream:
    content = yarn.choices[0].delta.content
    if content:
        print(content, end="", flush=True)

# Get full Ansa after stream completes
ansa = stream.get_ansa()
print(f"\nModel: {ansa.model}")
print(f"Tokens: {ansa.usage.total_tokens}")
print(f"Cost: ₦{ansa.cost.naira:.6f}")
print(f"ID: {ansa.id}")
```

---

## The Ansa Response Object

Every `gist()` call returns an `Ansa` object:

```python
ansa = client.gist(model="gemini/gemini-3.5-flash-lite", messages="How you dey?")

# Response
ansa.text               # response text
ansa.model              # model that served the request
ansa.reasoning          # thinking trace (reasoning models only)
ansa.tools              # tool calls (agent models only)
ansa.citations          # citations (search models only)
ansa.finish_reason      # why generation stopped

# Usage
ansa.usage.prompt_tokens      # input tokens used (includes system message)
ansa.usage.completion_tokens  # output tokens used
ansa.usage.total_tokens       # total tokens used

# Cost — Naira first
ansa.cost.naira         # total cost in Naira ← primary
ansa.cost.naira_input   # input cost in Naira
ansa.cost.naira_output  # output cost in Naira

# Identity
ansa.is_local                # True — runs on Nigerian hardware
ansa.is_ngn_data_residency   # True — data never leaves Nigeria
ansa.id                      # unique request ID (confam-xxxx-xxxx)

# Response metadata
ansa.raw                     # dict with id, finish_reason, usage
ansa.raw["id"]                # provider response ID
ansa.raw["finish_reason"]    # why generation stopped
ansa.raw["usage"]            # prompt and completion token counts
```

> **Note:** `prompt_tokens` includes any system message tokens. This is standard behaviour across all LLM providers (OpenAI, Anthropic, etc.).

---

## Embeddings

Generate embeddings with `client.embed()`. The shape of what you get back mirrors the shape of what you send in: a single string returns one flat vector, a list returns a list of vectors.

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-xxx")

# Single string in → one flat vector out
result = client.embed(
    model="liquid/lfm-2.5-embedding-350m:free",
    input="How you dey?"
)

print(result.embeddings)       # [0.123, -0.456, ...]
print(f"Cost: ₦{result.cost.naira:.6f}")
print(f"Tokens: {result.usage.total_tokens}")

# List in → list of vectors out, always — even with one item
result = client.embed(
    model="liquid/lfm-2.5-embedding-350m:free",
    input=["How you dey?", "Wetin dey happen?"]
)

print(len(result.embeddings))  # 2
```

### Task types

Some embedding models expect a task-type hint (e.g. `"query"` vs. `"document"`) to produce better embeddings for retrieval use cases. This defaults sensibly server-side if omitted — only pass it if you need a specific one:

```python
result = client.embed(
    model="liquid/lfm-2.5-embedding-350m:free",
    input="find me a good jollof rice recipe",
    task_type="query"
)

print(result.task_type_applied)  # confirms what actually happened for this call
```

`task_type_applied` is `None` when the requested model doesn't use task-type hints at all — the field itself tells you whether it had any effect, no separate capability lookup needed.

### The EmbeddingResult Object

```python
result = client.embed(model="liquid/lfm-2.5-embedding-350m:free", input="How you dey?")

result.embeddings            # vector(s) — shape matches your input shape
result.model                 # model that served the request
result.usage.prompt_tokens   # input tokens used
result.usage.total_tokens    # total tokens used (embeddings have no output tokens to bill)
result.cost.naira            # total cost in Naira
result.cost.naira_input      # input cost in Naira
result.is_local              # True — runs on Nigerian hardware
result.is_ngn_data_residency # True — data never leaves Nigeria
result.task_type_applied     # which task-type hint was actually applied, if any
result.id                    # unique request ID
result.raw                   # full raw response
```

---

## Models

#### Free Tier

| Model | Modality | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `gemini/gemini-3.1-flash-lite` | Text/Image/Video/File/Audio -> Text | ₦0 | ₦0| ₦0 | ₦0 |
| `gemini/gemini-3.5-flash-lite` | Text/Image/Video/File/Audio -> Text |  ₦0 | ₦0| ₦0 | ₦0 |
| `nvidia/nemotron-3-super-120b-a12b:free` | Text -> Text | ₦0 | ₦0| ₦0 | ₦0 |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | Text -> Text | ₦0 | ₦0| ₦0 | ₦0 |

#### Paid Tier

| Model | Modality | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `deepseek/deepseek-v4.1-flash` | Text/Image -> Text | ₦704 | ₦2,813 | ₦0.704 | ₦2.813 |

### Embeddings

#### Free Tier

| Model | Modality | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `liquid/lfm-2.5-embedding-350m:free` | Text -> Embeddings | ₦0 | ₦0 | ₦0 | ₦0 |

#### Paid Tier

| Model | Modality | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `google/gemini-embedding-001` | Text -> Embeddings | ₦352 | ₦0 | ₦0.352 | ₦0 |
| `google/gemini-embedding-2` | Text/Image/File/Audio/Video -> Text | ₦469 | ₦0 | ₦0.469 | ₦0 |

More embedding models coming soon.

More models coming soon. Contact [hello@confamnode.com](mailto:hello@confamnode.com) for early access.

---

## Pricing

All prices are in Nigerian Naira (₦). No USD. No conversion needed.

| Tier | How it works |
|---|---|
| Free | Use immediately. No wallet needed. Shared capacity. |
| Paid | Contact us to get access. Pay in Naira. No subscription. No expiry. |

**Currently in private beta.**
To get API access: [hello@confamnode.com](mailto:hello@confamnode.com)

---

## Rate Limits

Rate limits vary by plan. Contact [hello@confamnode.com](mailto:hello@confamnode.com).

- **Free tier** — shared capacity with lower limits
- **Paid tier** — dedicated higher limits

---

## System Message

ConfamNode adds a default system message to every request giving the model a Nigerian identity and context. This is standard behaviour across all LLM providers and is counted in `prompt_tokens`.

```python
# Use ConfamNode default identity (default)
ansa = client.gist(
    model="gemini/gemini-3.5-flash-lite",
    messages="Who are you?"
)
# "I am ConfamNode, Nigeria's AI inference gateway..."

# Override with your own system message
ansa = client.gist(
    model="gemini/gemini-3.5-flash-lite",
    messages="Who are you?",
    system="You are a helpful customer service agent for Konga."
)

# Disable system message entirely
ansa = client.gist(
    model="gemini/gemini-3.5-flash-lite",
    messages="Who you be?",
    system=None
)
```

---

## Caching

Caching is controlled **per request** and is **off by default** — every call returns a fresh response, even when the request is identical. This keeps data-generation loops and any workflow that resends the same prompt from getting the same cached answer back each time.

Pass `cache=True` to let the gateway serve and store a cached response — useful for idempotent lookups:

```python
# Default — caching off, fresh response every call
ansa = client.gist(
    model="deepseek/deepseek-v4.1-flash",
    messages="How you dey?"
)

# Enable caching — the gateway may return a stored response for a
# matching request, and store this one for next time
ansa = client.gist(
    model="deepseek/deepseek-v4.1-flash",
    messages="How you dey?",
    cache=True
)
```

Caching must be enabled for your account for `cache=True` to take effect. A cache hit returns near-instantly — the quickest way to see it is to send the **same** request twice with `cache=True`: the first call populates the cache, the second is served from it.

> **Note:** a cache hit still bills the full Naira cost of the request — you're paying for inference value, not raw compute. Caching saves time, not money.

---

## Reasoning Models

- nvidia/nemotron-3-super-120b-a12b:free
- nvidia/nemotron-3-ultra-550b-a55b:free
- gemini/gemini-3.1-flash-lite
- gemini/gemini-3.5-flash-lite
- deepseek/deepseek-v4.1-flash

Enable extended thinking for complex problems:

```python
ansa = client.gist(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages="One trader buy goods for ₦50,000 sell am for ₦75,000. After e pay ₦5,000 for transport and ₦3,000 for market, wetin be the real profit? Show how you calculate am.",
    reasoning_effort="low"
    # one of: "high", "medium", "low", "minimal", "none"
)

print(ansa.reasoning)   # thinking trace
print(ansa.text)        # final answer
```

Also available on reasoning models for more complex multi-step problems:

```python
ansa = client.gist(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages="Analyse the financial risk of a Nigerian fintech expanding to Ghana...",
    reasoning_effort="high"
)

print(ansa.reasoning)   # full thinking trace
print(ansa.text)        # final analysis
```

---

## Working with Images

```python
def encode_image_b64(image_path: Path) -> tuple[str, str]:
    """Returns (base64_data, mime_type)."""
    mime = "image/jpeg"
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        mime = "image/png"
    elif suffix == ".webp":
        mime = "image/webp"
    elif suffix in (".jpg", ".jpeg"):
        mime = "image/jpeg"
    data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return data, mime

image_path = Path("<image_path>")
img_b64, mime = encode_image_b64(image_path)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{img_b64}"}
            }
        ],
    },
]

ansa = client.gist(
    model="gemini/gemini-3.1-flash-lite",
    messages=messages
)

if ansa.reasoning:
    print(f"***Reasoning Start***\n{ansa.reasoning}\n***Reasoning End***")
print(ansa.text)
```
---

## Environment Variable

```bash
export CONFAMNODE_API_KEY="confam-xxx"
```

```python
# No need to pass api_key explicitly
client = ConfamNode()
```

---

## Custom Base URL

For enterprise clients running ConfamNode on private infrastructure:

```python
client = ConfamNode(
    api_key="confam-xxx",
    base_url="http://your-private-server:4000/v1"
)
```

---

## Error Handling

```python
from confamnode import (
    ConfamAuthError,
    ConfamRateLimitError,
    ConfamModelError,
    ConfamInsufficientBalanceError,
    ConfamProviderError,
    ConfamRequestError,
    ConfamNodeError
)

try:
    ansa = client.gist(
        model="gemini/gemini-3.5-flash-lite",
        messages="How you dey?"
    )
except ConfamAuthError:
    print("Check your API key")
except ConfamInsufficientBalanceError:
    print("Wallet balance too low. Top up to continue.")
except ConfamRateLimitError:
    print("You don reach your limit. Contact hello@confamnode.com")
except ConfamModelError:
    print("Invalid model name")
except ConfamProviderError:
    print("The AI provider is temporarily unavailable. Try again shortly.")
except ConfamRequestError:
    print("Request could not be processed — check your parameters")
except ConfamNodeError as e:
    print(f"Something went wrong: {e}")
```

All specific exceptions above are subclasses of `ConfamNodeError` — catching that alone is enough if you don't need to distinguish error types.

---

## Private AI Deployment

Need data-residential private AI on your own infrastructure?

JoTeq the First offers:
- On-premise deployment on Jetson devices and GPUs
- RTX 3090/4090 bare metal setup
- RAG pipelines and fine-tuning
- Dedicated hosted models
- SSH remote deployment

Contact: [hello@confamnode.com](mailto:hello@confamnode.com)

---

## Links

- Website: [confamnode.com](https://confamnode.com)
- PyPI: [pypi.org/project/confamnode](https://pypi.org/project/confamnode)
- GitHub: [github.com/confamnodeai/confamnode](https://github.com/confamnodeai/confamnode)
- General: [hello@confamnode.com](mailto:hello@confamnode.com)
- Support: [support@confamnode.com](mailto:support@confamnode.com)
- Billing: [billing@confamnode.com](mailto:billing@confamnode.com)

---

## License

Apache 2.0

---