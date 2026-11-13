# Microsoft open-sourced an AI quant lab. 50K stars on GitHub.

Here are both 👇

Qlib: https://github.com/microsoft/qlib
RD-Agent: https://github.com/microsoft/RD-Agent

First 3 steps:
1. pip install pyqlib, then follow the Quick Start in the Qlib README. Note: the official sample dataset is temporarily disabled; the README links a community data source to use instead.
2. Run one of the example workflows (e.g. the LightGBM benchmark) end to end before changing anything, so you know what "working" looks like.
3. Only then try RD-Agent (pip install rdagent). It needs an LLM API key and will spend tokens on every loop, so set a budget first.

One warning from our own tests: every new factor the agent finds is a new chance to fool yourself. Keep a locked test period and check results after real costs.

## Sources
GitHub API 2026-11-12: microsoft/qlib 50,232 stars MIT; microsoft/RD-Agent 15,347 stars MIT. Qlib + RD-Agent READMEs (pip install pyqlib / rdagent; dataset notice; "auto quant factory"; ML paradigms). Own result: 24 strategies, 0 passed (2026-11-12).
