# ConfamNode

The Nigerian AI inference gateway — access powerful AI models.

Built by **JoTeq the First**

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
python -m venv .venv

# Activate — Linux/Mac
source .venv/bin/activate

# Activate — Windows
.venv\Scripts\activate

# Install
pip install confamnode
```

### Using uv with virtual environment
```bash
# Create project with uv
uv init my-project
cd my-project

# Add confamnode
uv add confamnode

# Run your script
uv run python main.py
```

---

## Quick Start

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-sk-xxx")

ansa = client.gist(
    model="confam-speed",
    messages="How far?"
)

print(ansa.choices[0].message.content)
```

---

## Streaming

```python
for yarn in client.gist(
    model="confam-speed",
    messages="How far?",
    stream=True
):
    print(yarn.choices[0].delta.content, end="")
```

---

## Models

| Model | Description |
|---|---|
| `confam-lite` | Light text and general chat |
| `confam-speed` | Fast, high quality responses |
| `confam-reasoning` | Deep thinking and analysis |
| `confam-nano` | Private, NDPA compliant |
| `confam-embed-text-local` | Local CPU embeddings |

---

## Environment Variable

```bash
export CONFAMNODE_API_KEY="confam-sk-xxx"
```

```python
client = ConfamNode()
```

---

## Error Handling

```python
from confamnode import ConfamAuthError, ConfamRateLimitError, ConfamModelError

try:
    ansa = client.gist(
        model="confam-speed",
        messages="How far?"
    )
except ConfamAuthError:
    print("You sure say na the correct API Key be that")
except ConfamRateLimitError:
    print("You don reach your limit. Contact us at confamnode@gmail.com make we upgrade your plan")
except ConfamModelError:
    print("This model name no dey valid")
```

---

## Private Deployment

Need NDPA-compliant private AI on your own infrastructure? JoTeq the First offers on-premise deployment on Jetson devices and GPUs, RAG pipelines, fine-tuning, eevaluation, monitoring, and dedicated hosted models.

Contact us at **joteqthefirst@gmail.com**

---

## License

Apache License 2.0 

---