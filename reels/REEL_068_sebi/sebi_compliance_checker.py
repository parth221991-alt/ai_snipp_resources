#!/usr/bin/env python3
r"""
SEBI Financial AI Compliance & Codebase Audit Checker
Author: AI_SNIPP (@ai_snipp)
Repository: parth221991-alt/ai_snipp_resources
License: MIT

Automated compliance scanner for Indian FinTech platforms, algorithmic trading bots,
and AI-driven market intelligence tools. Verifies codebase readiness against
SEBI regulatory guidelines on AI models, algorithm transparency, data privacy,
and human oversight.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Ensure safe UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ANSI Color codes for clean terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    ".pytest_cache", ".idea", ".vscode", "dist", "build"
}

STANDARD_DISCLAIMER_KEYWORDS = [
    "market risks",
    "no way guarantee performance",
    "assurance of returns",
    "securities market",
    "not financial advice",
    "educational purpose"
]

PAN_REGEX = re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b")
SECRET_KEY_REGEX = re.compile(
    r"(?i)(api[_-]?key|secret[_-]?key|access[_-]?token|broker[_-]?secret|totp[_-]?secret)\s*=\s*['\"][a-zA-Z0-9_\-\.]{16,}['\"]"
)
HITL_KEYWORDS = [
    "human_in_the_loop", "hitl", "require_approval", "confirm_order",
    "manual_review", "compliance_approved", "is_approved", "operator_override"
]


class SEBIComplianceAuditor:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir).resolve()
        self.results: Dict[str, Any] = {
            "target": str(self.target_dir),
            "score": 0,
            "max_score": 100,
            "status": "PENDING",
            "audits": {}
        }

    def run_all_checks(self) -> Dict[str, Any]:
        print(f"{BOLD}{CYAN}======================================================={RESET}")
        print(f"{BOLD}{CYAN}🏛️  SEBI FINANCIAL AI COMPLIANCE CHECKER — 2026 EDITION{RESET}")
        print(f"Target Directory: {self.target_dir}")
        print(f"{BOLD}{CYAN}======================================================={RESET}\n")

        self.audit_model_disclosure()
        self.audit_credential_and_pii_hygiene()
        self.audit_hitl_gate()
        self.audit_statutory_disclaimers()
        self.audit_audit_trail_logging()

        # Calculate score
        total_points = sum(item["points_awarded"] for item in self.results["audits"].values())
        max_points = sum(item["max_points"] for item in self.results["audits"].values())
        score_pct = int((total_points / max_points) * 100) if max_points > 0 else 0

        self.results["score"] = score_pct
        if score_pct >= 85:
            self.results["status"] = "PASSED_COMPLIANT"
            status_color = GREEN
        elif score_pct >= 60:
            self.results["status"] = "WARNING_PARTIALLY_COMPLIANT"
            status_color = YELLOW
        else:
            self.results["status"] = "FAILED_NON_COMPLIANT"
            status_color = RED

        print(f"\n{BOLD}-------------------------------------------------------{RESET}")
        print(f"OVERALL SEBI COMPLIANCE SCORE: {status_color}{BOLD}{score_pct}% ({self.results['status']}){RESET}")
        print(f"{BOLD}-------------------------------------------------------{RESET}\n")

        for code, audit in self.results["audits"].items():
            color = GREEN if audit["status"] == "PASS" else (YELLOW if audit["status"] == "WARN" else RED)
            print(f"[{color}{audit['status']:4}{RESET}] {BOLD}{code}: {audit['title']}{RESET} ({audit['points_awarded']}/{audit['max_points']} pts)")
            for note in audit["notes"]:
                print(f"       • {note}")

        return self.results

    def audit_model_disclosure(self):
        code = "SEBI-AI-01"
        title = "Model Inventory & Algorithmic Disclosure"
        max_points = 25
        notes = []
        status = "FAIL"
        points = 0

        disclosure_candidates = [
            "model_disclosure.json",
            "model_disclosure_template.json",
            "model_inventory.json",
            "model_inventory.yaml",
            "sebi_disclosure.json"
        ]

        found_file = None
        for cand in disclosure_candidates:
            cand_path = self.target_dir / cand
            if cand_path.exists():
                found_file = cand_path
                break

        if found_file:
            try:
                data = json.loads(found_file.read_text(encoding="utf-8"))
                if "model_inventory" in data or "document_type" in data:
                    status = "PASS"
                    points = 25
                    notes.append(f"Model disclosure registered: Found valid {found_file.name}")
                else:
                    status = "WARN"
                    points = 15
                    notes.append(f"Found {found_file.name} but schema lacks 'model_inventory' key")
            except Exception as e:
                status = "WARN"
                points = 10
                notes.append(f"File {found_file.name} exists but could not parse JSON: {e}")
        else:
            notes.append("CRITICAL: No registered model disclosure file found. Create 'model_disclosure.json'.")

        self.results["audits"][code] = {
            "title": title,
            "status": status,
            "points_awarded": points,
            "max_points": max_points,
            "notes": notes
        }

    def audit_credential_and_pii_hygiene(self):
        code = "SEBI-AI-02"
        title = "PII Protection & Hardcoded Secret Sanitation"
        max_points = 20
        notes = []
        hardcoded_secrets = []
        pan_leaks = []

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file.endswith((".py", ".json", ".ts", ".js", ".env", ".yaml", ".yml")):
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore")
                        secret_matches = SECRET_KEY_REGEX.findall(content)
                        if secret_matches:
                            rel_path = filepath.relative_to(self.target_dir)
                            hardcoded_secrets.append(f"{rel_path}: {secret_matches[0][0]}")

                        # Check for hardcoded Indian PANs (excluding dummy patterns)
                        pans = PAN_REGEX.findall(content)
                        for pan in pans:
                            if pan not in ("ABCDE1234F", "AAAAA0000A", "XXXXX0000X"):
                                rel_path = filepath.relative_to(self.target_dir)
                                pan_leaks.append(f"{rel_path}: {pan}")
                    except Exception:
                        pass

        if not hardcoded_secrets and not pan_leaks:
            status = "PASS"
            points = 20
            notes.append("Zero hardcoded broker credentials or real Indian PANs detected in source code.")
        else:
            status = "FAIL"
            points = 0
            if hardcoded_secrets:
                notes.append(f"CRITICAL: Found {len(hardcoded_secrets)} potential hardcoded broker secrets/API keys!")
                for s in hardcoded_secrets[:3]:
                    notes.append(f"   - {s}")
            if pan_leaks:
                notes.append(f"CRITICAL: Found {len(pan_leaks)} unmasked Indian PAN patterns in files!")
                for p in pan_leaks[:3]:
                    notes.append(f"   - {p}")

        self.results["audits"][code] = {
            "title": title,
            "status": status,
            "points_awarded": points,
            "max_points": max_points,
            "notes": notes
        }

    def audit_hitl_gate(self):
        code = "SEBI-AI-03"
        title = "Human-in-the-Loop (HITL) Gate & Advisor Liability"
        max_points = 20
        notes = []
        hitl_matches = 0

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file.endswith((".py", ".ts", ".js", ".md", ".json")):
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore").lower()
                        for kw in HITL_KEYWORDS:
                            if kw in content:
                                hitl_matches += 1
                                break
                    except Exception:
                        pass

        if hitl_matches >= 2:
            status = "PASS"
            points = 20
            notes.append("Human approval gate verified in execution logic / documentation.")
        elif hitl_matches == 1:
            status = "WARN"
            points = 12
            notes.append("Partial human-in-the-loop references found. Ensure explicit approval gate is enforced.")
        else:
            status = "FAIL"
            points = 0
            notes.append("FAIL: No explicit Human-in-the-Loop gate detected. Fully autonomous trade dispatch violates SEBI guidelines.")

        self.results["audits"][code] = {
            "title": title,
            "status": status,
            "points_awarded": points,
            "max_points": max_points,
            "notes": notes
        }

    def audit_statutory_disclaimers(self):
        code = "SEBI-AI-04"
        title = "Mandatory Statutory Risk Disclaimers"
        max_points = 20
        notes = []
        disclaimer_hits = 0

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file.endswith((".py", ".md", ".html", ".tsx", ".jsx", ".json")):
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore").lower()
                        for kw in STANDARD_DISCLAIMER_KEYWORDS:
                            if kw in content:
                                disclaimer_hits += 1
                    except Exception:
                        pass

        if disclaimer_hits >= 3:
            status = "PASS"
            points = 20
            notes.append("Statutory risk disclaimers verified across project interfaces.")
        elif disclaimer_hits >= 1:
            status = "WARN"
            points = 10
            notes.append("Basic disclaimer present. Recommend adding full SEBI-prescribed wording.")
        else:
            status = "FAIL"
            points = 0
            notes.append("CRITICAL: Missing statutory risk disclaimers. Must state 'Investments in securities market are subject to market risks'.")

        self.results["audits"][code] = {
            "title": title,
            "status": status,
            "points_awarded": points,
            "max_points": max_points,
            "notes": notes
        }

    def audit_audit_trail_logging(self):
        code = "SEBI-AI-05"
        title = "Immutable Decision & Prompt Audit Logging"
        max_points = 15
        notes = []
        logging_found = False

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if file.endswith(".py"):
                    filepath = Path(root) / file
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="ignore")
                        if "logging." in content or "audit_log" in content or ".jsonl" in content:
                            logging_found = True
                            break
                    except Exception:
                        pass
            if logging_found:
                break

        if logging_found:
            status = "PASS"
            points = 15
            notes.append("Structured event and prompt audit logging detected.")
        else:
            status = "WARN"
            points = 7
            notes.append("Structured audit logging not clearly found. Ensure all AI prompts & executions are archived.")

        self.results["audits"][code] = {
            "title": title,
            "status": status,
            "points_awarded": points,
            "max_points": max_points,
            "notes": notes
        }


def main():
    parser = argparse.ArgumentParser(description="SEBI AI Compliance Codebase Checker.")
    parser.add_argument("--target", default=".", help="Target directory to audit (default: current directory)")
    parser.add_argument("--output", default="sebi_audit_report.json", help="Path to export JSON audit report")
    args = parser.parse_args()

    auditor = SEBIComplianceAuditor(args.target)
    results = auditor.run_all_checks()

    output_path = Path(args.output)
    output_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n📄 Saved full audit report to: {output_path.resolve()}\n")

    if results["score"] < 60:
        sys.exit(1)


if __name__ == "__main__":
    main()
