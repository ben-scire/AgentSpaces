# Inspired by message-passing patterns used in AgentSpaces communication workflow

# AgentSpaces

Lightweight, typed message-passing engine for building modular agent pipelines.

## Why it exists

Pulled from my experience automating complex design workflows — this is the minimal skeleton I wish I had at the start.

## Quickstart

python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
python -m agentspaces.examples.echo_pipeline
pytest -q

## Architecture

contracts.py → message schema (AgentMsg)
agent.py → base class
bus.py → in-process pub/sub
memory.py → per-agent KV store
logging.py → structured JSON logs

## Philosophy

AgentSpaces favors explicit contracts, deterministic behavior, and production ergonomics without excess abstraction.
