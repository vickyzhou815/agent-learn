# Day 1 Notes — OpenAI SDK Basics

## 1. `load_dotenv()` and Environment Variables

```python
from dotenv import load_dotenv
load_dotenv()
```

`load_dotenv()` reads `.env` file and injects its key-value pairs into the process's environment variables — the same place the OS stores things like `PATH`. After this call, `OPENAI_API_KEY` is accessible anywhere in process via `os.getenv("OPENAI_API_KEY")`.

**Flow:**
```
.env file
    ↓
load_dotenv()
    ↓
Environment Variables (OS-level, in-process)
    ↓
accessible via os.getenv(...)
```

---

## 2. `OpenAI()` — What Happens Under the Hood

```python
client = OpenAI()
```

Conceptually, the SDK does something like this internally:

```python
class OpenAI:
    def __init__(self):
        self.api_key  = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.timeout  = 60
```

The `client` object is **configuration + state + functionality** bundled together. You never pass `api_key=...` again on every call — the client already holds it.

---

## 3. `client.responses` vs `client.chat.completions`

These are **two different APIs** exposed by the same client object:

| | `client.chat.completions` | `client.responses` |
|---|---|---|
| **API** | Chat Completions API (older) | Responses API (newer, 2025) |
| **Style** | Stateless — you manage history manually | Stateful — SDK can track conversation |
| **Usage** | `client.chat.completions.create(...)` | `client.responses.create(...)` |
| **Input key** | `messages=[...]` | `input="..."` |

```python
# Older style
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Newer style
response = client.responses.create(
    model="gpt-4o",
    input="Hello"
)
```

Both live on the same `client` object — think of them as two namespaces, like two subsystems on the same C++ object:

```cpp
client.fileSystem.read(...)
client.network.send(...)
```

---

## Key Mental Model

```
.env
 ↓
load_dotenv()          # inject into environment
 ↓
os.getenv("OPENAI_API_KEY")   # SDK reads this internally
 ↓
OpenAI()               # stores api_key, base_url, timeout inside object
 ↓
client.responses.create(...)  # uses stored config, no re-authentication needed
```