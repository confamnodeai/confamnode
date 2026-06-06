# ConfamNode

The Nigerian AI inference SDK — access powerful AI models and pay in Naira.

Built by **JoTeq the First**

---

## Installation

```bash
pip install confamnode
```

---

## Quick Start

```python
from confamnode import ConfamNode

client = ConfamNode(api_key="confam-sk-xxx")

response = client.gist(
    model="confam-speed",
    messages="How far?"
)

print(response.choices[0].message.content)
```

---

## Streaming

```python
for chunk in client.gist(
    model="confam-speed",
    messages="How far?",
    stream=True
):
    print(chunk.choices[0].delta.content, end="")
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
    response = client.gist(
        model="confam-speed",
        messages="How far?"
    )
except ConfamAuthError:
    print("Check your API key")
except ConfamRateLimitError:
    print("You don reach your limit. To upgrade your plan, contact us at confamnode@gmail.com")
except ConfamModelError:
    print("Invalid model name")
```

---

## Private Deployment

Need NDPA-compliant private AI on your own infrastructure? JoTeq the First offers on-premise deployment on Jetson devices and GPUs, RAG pipelines, fine-tuning, and dedicated hosted models.

Contact us at **joteqthefirst@gmail.com**

---

## License

Apache License 2.0 

---