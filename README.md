# RPG Story Generator

This repository hosts the development of a logic-driven suspense RPG generator.

```
/core   - Python backend implementation
/webui  - Next.js frontend (placeholder)
/docs   - Project documentation
```

## LLM Client

The backend exposes a small wrapper `OpenRouterClient` in `rpggen.llm_client`. It
uses [LangChain](https://python.langchain.com/) to talk to the OpenRouter API and
supports automatic retries and optional streaming output.

```python
from rpggen.llm_client import OpenRouterClient

# will read OPENROUTER_* variables from .env
client = OpenRouterClient(streaming=True)
for token in client.stream("Hello world"):
    ...  # handle streamed tokens
```

Create a ``.env`` file based on ``.env.example`` to configure
``OPENROUTER_API_KEY``, ``OPENROUTER_BASE_URL`` and ``OPENROUTER_MODEL``.

