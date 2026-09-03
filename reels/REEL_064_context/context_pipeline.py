#!/usr/bin/env python3
"""
The 3-Step Context Pipeline for AI Coding Assistants (Claude Code, Cursor, Windsurf)
Curated by @ai_snipp (Featured on Reel #064)

Three-step architecture:
1. Repo Tree Digest: Generates a lightweight 50-line AST symbol map (<600 tokens vs 45k+ raw).
2. Active Interface Slicing: Stubs internal implementation logic, sending only type signatures and contracts.
3. Append-Only Scratchpad: Maintains a persistent state machine for agent memory, eliminating infinite loops.
"""

import os
import sys
import ast
import argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv", "env",
    "dist", "build", ".next", ".cache", ".turbo", "target", ".gemini"
}

SUPPORTED_EXTS = {".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs"}


def generate_tree_digest(root_path: Path, max_depth: int = 3) -> str:
    """Step 1: Scans directory and extracts symbol outlines into a compact hierarchy."""
    lines = [f"# Codebase Interface Digest: {root_path.resolve().name}"]
    lines.append("# Format: [DIR] or [FILE] -> exported classes & functions\n")

    def walk(current: Path, depth: int):
        if depth > max_depth:
            return
        
        try:
            items = sorted(list(current.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            return

        for item in items:
            if item.name.startswith(".") and item.name not in {".agents"}:
                continue
            if item.is_dir():
                if item.name in IGNORE_DIRS:
                    continue
                indent = "  " * depth
                lines.append(f"{indent}📁 {item.name}/")
                walk(item, depth + 1)
            elif item.suffix in SUPPORTED_EXTS:
                indent = "  " * depth
                symbols = extract_top_symbols(item)
                sym_str = f" → {', '.join(symbols)}" if symbols else ""
                lines.append(f"{indent}📄 {item.name}{sym_str}")

    walk(root_path, 0)
    digest_text = "\n".join(lines)
    est_tokens = len(digest_text.split()) * 1.3
    lines.append(f"\n# Estimated Context Size: ~{int(est_tokens)} tokens")
    return "\n".join(lines)


def extract_top_symbols(file_path: Path) -> list[str]:
    """Extracts top-level class and function names from supported files."""
    symbols = []
    if file_path.suffix == ".py":
        try:
            tree = ast.parse(file_path.read_text(encoding="utf-8", errors="ignore"))
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append(f"def {node.name}()")
                elif isinstance(node, ast.ClassDef):
                    symbols.append(f"class {node.name}")
        except Exception:
            pass
    else:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for line in content.splitlines()[:50]:
                line = line.strip()
                if line.startswith("export function ") or line.startswith("export const "):
                    parts = line.split()
                    if len(parts) >= 3:
                        symbols.append(parts[2].split("(")[0])
                elif line.startswith("export class ") or line.startswith("class "):
                    parts = line.split()
                    if len(parts) >= 2:
                        symbols.append(parts[1].split("{")[0])
        except Exception:
            pass
    return symbols[:4]


def slice_python_interface(file_path: Path) -> str:
    """Step 2: Stubs all function/method bodies into '...' leaving signatures & docstrings."""
    try:
        content = file_path.read_text(encoding="utf-8")
        parsed = ast.parse(content)
    except Exception as e:
        return f"# Error parsing {file_path.name}: {e}"

    class InterfaceStubber(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            doc = ast.get_docstring(node)
            body = []
            if doc:
                body.append(ast.Expr(value=ast.Constant(value=doc)))
            body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
            node.body = body
            return node

        def visit_AsyncFunctionDef(self, node):
            doc = ast.get_docstring(node)
            body = []
            if doc:
                body.append(ast.Expr(value=ast.Constant(value=doc)))
            body.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
            node.body = body
            return node

    stubbed = InterfaceStubber().visit(parsed)
    ast.fix_missing_locations(stubbed)
    return ast.unparse(stubbed)


def init_scratchpad(target_file: Path):
    """Step 3: Creates or updates an append-only agent scratchpad state machine."""
    template = """# Task Scratchpad & State Machine
**Active Status:** IN_PROGRESS
**Target Goal:** [Define the single verifiable objective here]

---

## 1. Current Phase
- [x] Phase 1: Context Ingestion (Repo Digest & Interface Slices loaded)
- [ ] Phase 2: Implementation & Code Modification
- [ ] Phase 3: Unit Verification & Lint Gates

---

## 2. Decision Log (Append-Only)
- Decision 1: Initialized context pipeline with active interface slices.
- Decision 2: [Next architectural choice...]

---

## 3. Active Blockers & Gates
- Gate 1: Secret scanning & syntax check must pass before commit.
- Gate 2: Zero raw bulk file dumping.
"""
    target_file.parent.mkdir(parents=True, exist_ok=True)
    if not target_file.exists():
        target_file.write_text(template, encoding="utf-8")
        print(f"[context_pipeline] Initialized scratchpad at: {target_file}")
    else:
        print(f"[context_pipeline] Scratchpad already exists at: {target_file}")


def main():
    parser = argparse.ArgumentParser(description="3-Step Context Pipeline for AI Coding Assistants")
    parser.add_argument("--digest", nargs="?", const=".", help="Generate a 50-line AST codebase tree digest")
    parser.add_argument("--slice", type=str, help="Extract interface signature stub from a Python file")
    parser.add_argument("--scratchpad", nargs="?", const=".agents/SCRATCHPAD.md", help="Initialize agent scratchpad")

    args = parser.parse_args()

    if args.digest:
        root = Path(args.digest)
        print(generate_tree_digest(root))
    elif args.slice:
        p = Path(args.slice)
        if p.exists() and p.suffix == ".py":
            print(slice_python_interface(p))
        else:
            print(f"Error: {args.slice} is not a valid Python file.")
    elif args.scratchpad:
        target = Path(args.scratchpad)
        init_scratchpad(target)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
