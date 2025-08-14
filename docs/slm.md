# Sovereign Local Model (SLM)

The `slm` module is responsible for integrating the Sovereign Local Model (SLM) into the research workflow.

## The SLM Orchestrator

The `src/slm/orchestrator.py` script is the main entry point for interacting with the SLM. This script is responsible for loading the SLM, managing the conversation history, and calling the appropriate tools based on the user's input.

## SLM Tools

The `src/slm/tools.py` script defines the "tool-use DSL" that the SLM can call. These tools allow the SLM to interact with the other parts of the system. For example, there are tools for:

*   Generating features
*   Running backtests
*   Creating reports

By using these tools, the SLM can automate many of the tedious tasks that are involved in quantitative research.

## Recommended SLMs

Any 1-7B instruct model in GGUF format should work for this project. The SLM is used for orchestration and text-to-code, so you don't need a massive model.
