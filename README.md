# AI Coding Agent

A command-line AI coding agent written in Python. You give it a task in plain English; it plans a sequence of tool calls (list files, read files, write files, run Python scripts), executes them in a loop, and reports back. Every file operation is confined to a single sandboxed working directory.

It talks to LLMs through the [OpenRouter](https://openrouter.ai) API using the OpenAI Python SDK and its **function calling** interface.

## How it works

```
 user prompt ──► LLM (OpenRouter) ──► tool call? ──yes──► call_function() ──► result
                      ▲                    │                                  │
                      └────────────────────┴──────────── append to messages ◄──┘
                                           │ no
                                           ▼
                                    print final answer
```

1. `main.py` sends the system prompt and your prompt to the model, along with the schemas of the available tools.
2. If the model replies with tool calls, `functions/call_function.py` dispatches each one, and the results are appended to the conversation.
3. The loop repeats (up to 20 iterations) until the model answers without requesting a tool.

## Tools available to the model

| Tool | Description |
|---|---|
| `get_files_info` | List files and directories with sizes |
| `get_file_content` | Read a file (truncated at 10,000 characters, see `config.py`) |
| `write_file` | Create or overwrite a file |
| `run_python_file` | Run a `.py` file with optional CLI arguments (30 s timeout) |

### Safety guardrails

- The working directory is injected by `call_function.py` (`./workspace`); the model cannot choose it.
- Every tool resolves the requested path and rejects anything that falls outside the working directory (path traversal such as `../` is blocked).
- Python execution is limited to `.py` files and times out after 30 seconds.

## Project structure

| Path | Description |
|---|---|
| `main.py` | CLI entry point and agent loop |
| `prompts.py` | System prompt |
| `config.py` | Settings (`MAX_CHARS` for file reads) |
| `functions/call_function.py` | Tool registry, dispatcher, working-directory injection |
| `functions/get_files_info.py` | Directory listing tool |
| `functions/get_file_content.py` | File reading tool |
| `functions/write_file.py` | File writing tool |
| `functions/run_python_file.py` | Python execution tool |

## Getting started

**Requirements:** Python 3.13+, [uv](https://docs.astral.sh/uv/) (or pip), and an [OpenRouter API key](https://openrouter.ai/keys).

```bash
# 1. Install dependencies
uv sync

# 2. Add your API key
echo 'OPENROUTER_API_KEY=your_key_here' > .env

# 3. Create the sandbox directory the agent works in
mkdir workspace
```

Put the code you want the agent to work on inside `workspace/` (any small Python project works).

## Usage

```bash
uv run main.py "your task here"
uv run main.py "your task here" --verbose
```

Examples:

```bash
uv run main.py "what files are in the project?"
uv run main.py "read main.py and explain what it does"
uv run main.py "fix the bug in the project and run the tests"
```

`--verbose` prints each tool call with its arguments, the tool results, and token usage.

## Configuration

- **Model:** set in `main.py` (`model="openrouter/free"`). Change it to any OpenRouter model that supports tool calling.
- **Working directory:** set in `functions/call_function.py` (currently `./workspace`).
- **Iteration limit:** 20 loop iterations in `main.py`.

## Tech stack

Python, OpenAI SDK (OpenRouter endpoint), python-dotenv, argparse, subprocess.

## Disclaimer

This agent can write files and execute code inside its working directory. Run it only on code you trust, and don't point it at directories containing sensitive data.
