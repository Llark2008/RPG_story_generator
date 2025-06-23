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

## Consistency Checker

The module `rpggen.consistency_checker` provides a small helper for retrieval
augmented consistency checks. It builds a FAISS index of reference texts and
asks an LLM to rate how well a given question is answered by those documents.

```python
from langchain_community.llms import FakeListLLM
from langchain_community.embeddings import FakeEmbeddings
from rpggen.consistency_checker import ConsistencyChecker

checker = ConsistencyChecker(
    llm=FakeListLLM(responses=["1.0"]),
    embeddings=FakeEmbeddings(size=3),
)
checker.build_index(["fact one", "fact two"])
score = checker.score("Is fact one mentioned?")
```

## Utility helpers

Common helpers are collected under `rpggen.utils`.

```python
from rpggen.utils.text import slugify, chinese_length
from rpggen.utils.id import hash_id
from rpggen.utils.log import get_logger

slug = slugify("Hello World!")
length = chinese_length("你好世界")
uid = hash_id("some text")
logger = get_logger("demo")
```

## Development

Install dependencies with [Poetry](https://python-poetry.org/):

```bash
poetry install --with dev
```

Run the linter and unit tests:

```bash
poetry run ruff check .
poetry run pytest -m "not slow"
```

JSON schema files under `core/rpggen/models` are generated automatically when
importing `rpggen.models`. CI verifies they are up to date.

## Pipeline CLI

The project ships with a Typer-based command line application to run
pipeline nodes. `node1` is the fully featured world generator while
`node2` remains a lightweight stub.

Example configuration files can be found in the `examples/` directory:

```
$ poetry run rpggen node1 --config examples/world.yml
$ poetry run rpggen node2 --config examples/chars.yml
$ poetry run rpggen all --config examples/config.yml
```

Each node is implemented by subclassing `BaseNode` which defines the standard
`load_inputs → build_prompt → call_llm → parse → check_consistency → save` flow
and built-in retry handling.

