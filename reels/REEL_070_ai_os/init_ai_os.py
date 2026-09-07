r"""
One-Click Private AI_OS Initializer & Scaffolding Tool
Author: @ai_snipp (Parametriq Lab)
License: MIT
"""

import os
import sys
import argparse
from pathlib import Path

FOLDERS = [
    "01_memory",
    "02_skills",
    "03_prompts",
    "04_projects",
    "05_content",
    "06_agents",
    "07_templates",
    "08_mcp",
    "09_docs"
]

CLAUDE_TEMPLATE = """# AI_OS — Operating Co-Founder & Executive Brief

Company / Workspace OS of a solo builder/founder running quantitative and AI products.
This file defines deterministic operating instructions for Antigravity IDE and Claude Code CLI.

---

## 1. Operating Principles
- **Determinism over prediction:** Prefer deterministic logic, explicit state machines, and hard gates before soft gates.
- **Append-only logs:** Record all critical state changes and task completions in `01_memory/MEMORY.md`.
- **Zero Raw Bulk Rule:** Never feed raw 500-line files or verbose terminal logs to high-tier models. Use a 50-line AST digest.

---

## 2. Model Tier Routing (Zero Metered Spend)
- **Tier 0 (Free):** Task Scheduler / Cron for fixed time automations.
- **Tier 1 (Free):** Python / PowerShell scripts for deterministic tasks.
- **Tier 2 (Free):** Pre-commit hooks, ruff, mypy, secret scanners.
- **Tier 3 (Free/Local):** Gemini CLI, Codex, Ollama for bulk digests and repository searches.
- **Tier 4 (Pro Sub):** Antigravity / Claude Code for architecture, core logic, and high-judgment execution.

---

## 3. Active Projects & Priorities
1. **Primary Product** — [Description of your main active project]
2. **Secondary Tooling** — [Internal infrastructure and automation]

---

## 4. Multi-Agent Executive Team
Refer to `06_agents/` for specialized agent roles:
- `06_agents/chief_of_staff.md`
- `06_agents/engineering_director.md`
- `06_agents/growth_director.md`
- `06_agents/research_lead.md`
"""

MEMORY_TEMPLATE = """# Workspace Memory & State Log

## Active Goals
- [ ] Initialize core product architecture
- [ ] Configure MCP tool connections
- [ ] Verify automated CI/CD test gates

## Key Architectural Decisions
- **2026-09-07:** Initialized AI_OS 9-folder workspace hierarchy.
"""

CHIEF_OF_STAFF_TEMPLATE = """# Chief of Staff Agent Spec

**Role:** Executive Orchestrator & Founder Interface  
**Mandate:** Coordinate company priorities across engineering, growth, and research directors.

## Operating Protocol:
1. Load state from `01_memory/MEMORY.md`.
2. Review portfolio priority order before assigning tasks.
3. Enforce Human-in-the-Loop gates on all production deployments.
"""

MCP_STARTER_TEMPLATE = """{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
"""

def scaffold_ai_os(target_dir: Path):
    print(f"Scaffolding AI_OS workspace in: {target_dir.resolve()}...")
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Create 9 numbered folders
    for folder in FOLDERS:
        fpath = target_dir / folder
        fpath.mkdir(exist_ok=True)
        # Add .gitkeep
        (fpath / ".gitkeep").touch(exist_ok=True)
        print(f"  [+] Created folder: {folder}/")

    # 2. Write CLAUDE.md & AGENTS.md
    claude_md = target_dir / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text(CLAUDE_TEMPLATE, encoding="utf-8")
        print("  [+] Created root CLAUDE.md")

    agents_md = target_dir / "AGENTS.md"
    if not agents_md.exists():
        agents_md.write_text(CLAUDE_TEMPLATE, encoding="utf-8")
        print("  [+] Created root AGENTS.md")

    # 3. Write memory & agent templates
    mem_file = target_dir / "01_memory" / "MEMORY.md"
    if not mem_file.exists():
        mem_file.write_text(MEMORY_TEMPLATE, encoding="utf-8")
        print("  [+] Created 01_memory/MEMORY.md")

    cos_file = target_dir / "06_agents" / "chief_of_staff.md"
    if not cos_file.exists():
        cos_file.write_text(CHIEF_OF_STAFF_TEMPLATE, encoding="utf-8")
        print("  [+] Created 06_agents/chief_of_staff.md")

    mcp_file = target_dir / "08_mcp" / "mcp_config.json"
    if not mcp_file.exists():
        mcp_file.write_text(MCP_STARTER_TEMPLATE, encoding="utf-8")
        print("  [+] Created 08_mcp/mcp_config.json")

    print("\n==========================================")
    print("AI_OS Workspace Initialization Complete!")
    print(f"Location: {target_dir.resolve()}")
    print("Next step: Open your terminal inside this folder and run `claude` or `antigravity`!")
    print("==========================================")

def main():
    parser = argparse.ArgumentParser(description="Initialize a Private AI_OS workspace in any directory.")
    parser.add_argument("--path", default=".", help="Target directory for AI_OS (default: current directory)")
    args = parser.parse_args()

    scaffold_ai_os(Path(args.path))

if __name__ == "__main__":
    main()
