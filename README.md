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

client = ConfamNode(api_key="confam-sk-xxx")

ansa = client.gist(
    model="confam-speed",
    messages="How you dey?"
)

print(ansa.text)
print(f"Cost:   ₦{ansa.cost.naira:.6f}")
print(f"Tokens: {ansa.usage.total_tokens}")
print(f"ID:     {ansa.id}")
```

---

## Streaming

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-sk-xxx")

stream = client.gist(
    model="confam-speed",
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
print(f"\nModel:  {ansa.model}")
print(f"Tokens: {ansa.usage.total_tokens}")
print(f"Cost:   ₦{ansa.cost.naira:.6f}")
if ansa.cost.dollars:
    print(f"${ansa.cost.dollars:.8f}")
print(f"ID: {ansa.id}")
```

---

## The Ansa Response Object

Every `gist()` call returns an `Ansa` object:

```python
ansa = client.gist(model="confam-speed", messages="How far?")

# Response
ansa.text               # response text
ansa.model              # model that served the request
ansa.reasoning          # thinking trace (reasoning models only)
ansa.tools              # tool calls (agent models only)
ansa.citations          # citations (search models only)
ansa.finish_reason      # why generation stopped

# Usage
ansa.usage.prompt_tokens      # input tokens used
ansa.usage.completion_tokens  # output tokens used
ansa.usage.total_tokens       # total tokens used

# Cost — Naira first
ansa.cost.naira         # total cost in Naira ← primary
ansa.cost.naira_input   # input cost in Naira
ansa.cost.naira_output  # output cost in Naira
ansa.cost.dollars       # cost in USD (if available)

# Identity
ansa.is_local                # True — runs on Nigerian hardware
ansa.is_ngn_data_residency   # True — data never leaves Nigeria
ansa.id                      # unique request ID (confam-xxxx-xxxx)
ansa.raw                     # original LiteLLM response
```

---

## Models

### Free Tier

| Model | Description | Price |
|---|---|---|
| `confam-lite` | Light text and general chat | Free |
| `confam-speed` | Fast, high quality responses | Free |
| `confam-reasoning` | Standard reasoning and analysis | Free |

### Paid Tier

| Model | Description | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `confam-intelligence` | General smart tasks, 1M context | ₦596 | ₦3,571 | ₦0.596 | ₦3.571 |
| `confam-deep-reasoning` | Complex thinking, multi-step analysis | ₦234 | ₦468 | ₦0.234 | ₦0.468 |
| `confam-code` | Coding assistance, 1M context | ₦234 | ₦468 | ₦0.234 | ₦0.468 |

### Local Models — Nigeria Data Residency

| Model | Description | Input ₦/1M | Output ₦/1M | Input ₦/1K | Output ₦/1K |
|---|---|---|---|---|---|
| `confam-nano` | Qwen3.5 4B on Jetson Orin Nano | ₦500 | ₦1,500 | ₦0.500 | ₦1.500 |

Runs entirely on Nigerian hardware. Data never transmitted abroad.

Data never leaves Nigeria. Ideal for banks, fintechs, hospitals, law firms, and government agencies.

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
- **confam-nano** — limited capacity, queue-based

---

## System Message

ConfamNode adds a default system message to every request giving the model a Nigerian identity and context. This is standard behaviour across all LLM providers and is counted in `prompt_tokens`.

```python
# Use ConfamNode default identity (default)
ansa = client.gist(
    model="confam-speed",
    messages="Who are you?"
)
# "I am ConfamNode, Nigeria's AI inference gateway..."

# Override with your own system message
ansa = client.gist(
    model="confam-speed",
    messages="Who are you?",
    system="You are a helpful customer service agent for Konga."
)

# Disable system message entirely
ansa = client.gist(
    model="confam-speed",
    messages="Who you be?",
    system=None
)
```

---

## Reasoning Models

Enable extended thinking for complex problems:

```python
ansa = client.gist(
    model="confam-reasoning",
    messages="One trader buy goods for ₦50,000 sell am for ₦75,000. After e pay ₦5,000 for transport and ₦3,000 for market, wetin be the real profit? Show how you calculate am.",
    # Explicit reasoning control
    allowed_openai_params=["reasoning_effort"],
    rreasoning_effort={"effort": "low", "summary": "detailed"} # effort can be "low", "mid", "high", or "xhigh". summary can be "detailed", or "concise"
)

print(ansa.reasoning)   # thinking trace
print(ansa.text)        # final answer
```

Also available on `confam-deep-reasoning` for more complex multi-step problems:

```python
ansa = client.gist(
    model="confam-deep-reasoning",
    messages="Analyse the financial risk of a Nigerian fintech expanding to Ghana...",
    # Explicit reasoning control
    allowed_openai_params=["reasoning_effort"],
    rreasoning_effort={"effort": "low", "summary": "detailed"} # effort can be "low", "mid", "high", or "xhigh". summary can be "detailed", or "concise"
)

print(ansa.reasoning)   # full thinking trace
print(ansa.text)        # final analysis
```

---

## RAG (Retrieval-Augmented Generation)

### Best models for RAG

| Model | Why | Context |
|---|---|---|
| `confam-intelligence` | General RAG, reliable, long context | 1M tokens |
| `confam-code` | Code search, documentation RAG | 1M tokens |
| `confam-deep-reasoning` | Complex RAG, multi-hop reasoning | 1M tokens |

---

## Data Residency

Nigerian businesses handling sensitive data can use local models that run entirely on Nigerian hardware — data is never transmitted abroad:

```python
ansa = client.gist(
    model="confam-nano",
    messages="Analyse this sensitive document..."
)

print(ansa.is_local)                 # True — runs on Nigerian hardware
print(ansa.is_ngn_data_residency)    # True — data never leaves Nigeria
print(ansa.text)
```

**Ideal for:**
- Nigerian banks and fintechs
- Healthcare companies
- Law firms
- Government agencies
- Any business with strict data residency requirements

---

## Environment Variable

```bash
export CONFAMNODE_API_KEY="confam-sk-xxx"
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
    api_key="confam-sk-xxx",
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
    ConfamNodeError
)

try:
    ansa = client.gist(
        model="confam-speed",
        messages="How you dey?"
    )
except ConfamAuthError:
    print("Check your API key")
except ConfamRateLimitError:
    print("You don reach your limit. Contact hello@confamnode.com")
except ConfamModelError:
    print("Invalid model name")
except ConfamNodeError as e:
    print(f"Something went wrong: {e}")
```

---

## Private AI Deployment

Need Data-residential private AI on your own infrastructure?

JoTeq the First offers:
- On-premise deployment on Jetson devices and GPUs
- RTX 3090/4090 bare metal setup
- RAG pipelines and fine-tuning
- Dedicated hosted models
- SSH remote deployment

Contact: [hello@confamnode.com](mailto:hello@confamnode.com)

---

## Links

- PyPI: [pypi.org/project/confamnode](https://pypi.org/project/confamnode)
- GitHub: [github.com/confamnodeai/confamnode](https://github.com/confamnodeai/confamnode)
- General: [hello@confamnode.com](mailto:hello@confamnode.com)
- Support: [support@confamnode.com](mailto:support@confamnode.com)
- Billing: [billing@confamnode.com](mailto:billing@confamnode.com)

---

## License

Apache 2.0

---