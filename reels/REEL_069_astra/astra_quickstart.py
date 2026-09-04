r"""
GPT-6 Astra Quickstart — cost calculator, model router, spend-cap guard, and a
computer-use request skeleton.

Featured on AI_SNIPP Reel #069.

Pricing (per 1M tokens, from launch coverage 2026-09-03):
    standard : $10 input  / $50 output
    fast     : $20 input  / $100 output

NOTE ON THE COMPUTER-USE CALL: OpenAI's public tool schema for Astra computer-use
was still being documented at launch. The skeleton below follows the shape of the
Responses API agent loop; treat the tool block as a placeholder and check the
current docs before relying on it.

Usage:
    pip install -r requirements.txt
    export OPENAI_API_KEY="sk-..."

    python astra_quickstart.py --estimate 200000 50000     # cost of 200K in / 50K out
    python astra_quickstart.py --estimate 200000 50000 --mode fast
    python astra_quickstart.py --route "extract dates from this invoice"
    python astra_quickstart.py --hello                     # live smoke test (needs access)

MIT License.
"""

from __future__ import annotations

import argparse
import functools
import os
import sys

MODEL_ID = "gpt-6-astra"
MODEL_ID_PRO = "gpt-6-astra-pro"

# USD per 1M tokens
PRICING = {
    "standard": {"input": 10.0, "output": 50.0},
    "fast": {"input": 20.0, "output": 100.0},
}

# A cheap model to hand the boring sub-steps to. Swap for whatever you actually run.
CHEAP_MODEL = os.environ.get("ASTRA_CHEAP_MODEL", "gpt-5.6-sol-mini")


# --------------------------------------------------------------------------------------
# 1. Cost calculator
# --------------------------------------------------------------------------------------
def estimate_cost(input_tokens: int, output_tokens: int, mode: str = "standard") -> dict:
    if mode not in PRICING:
        raise ValueError(f"mode must be one of {list(PRICING)}")
    p = PRICING[mode]
    in_cost = input_tokens / 1_000_000 * p["input"]
    out_cost = output_tokens / 1_000_000 * p["output"]
    total = in_cost + out_cost
    return {
        "mode": mode,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_cost_usd": round(in_cost, 4),
        "output_cost_usd": round(out_cost, 4),
        "total_usd": round(total, 4),
        "runs_per_dollar": round(1 / total, 1) if total else float("inf"),
    }


def monthly_projection(cost_per_run_usd: float, runs_per_day: int) -> dict:
    daily = cost_per_run_usd * runs_per_day
    return {
        "per_run_usd": round(cost_per_run_usd, 4),
        "runs_per_day": runs_per_day,
        "per_day_usd": round(daily, 2),
        "per_month_usd": round(daily * 30, 2),
    }


# --------------------------------------------------------------------------------------
# 2. Model router — keep Astra for the steps that need it
# --------------------------------------------------------------------------------------
FRONTIER_SIGNALS = (
    "plan", "decide", "architect", "debug", "reason about", "trade-off",
    "which approach", "multi-step", "browse", "use the computer", "navigate",
    "research and compare", "vulnerability", "prove", "derive",
)


def route(task: str) -> str:
    """Return the model id that should handle `task`.

    Heuristic only: if the task reads like planning / long-horizon / agentic work,
    send it to Astra; otherwise send it to the cheap model. Tune the signal list
    for your workload.
    """
    t = task.lower()
    if any(sig in t for sig in FRONTIER_SIGNALS):
        return MODEL_ID
    # short, mechanical extraction / formatting / classification -> cheap
    if len(t.split()) < 40:
        return CHEAP_MODEL
    return MODEL_ID


# --------------------------------------------------------------------------------------
# 3. Spend-cap guard
# --------------------------------------------------------------------------------------
class SpendCapExceeded(RuntimeError):
    pass


def spend_cap(max_usd_per_call: float, max_usd_total: float):
    """Decorator: block a call whose *estimated* cost exceeds the caps.

    The wrapped function must accept `est_input_tokens` and `est_output_tokens`
    kwargs and (optionally) a `mode` kwarg.
    """
    state = {"spent": 0.0}

    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, est_input_tokens=0, est_output_tokens=0, mode="standard", **kw):
            est = estimate_cost(est_input_tokens, est_output_tokens, mode)["total_usd"]
            if est > max_usd_per_call:
                raise SpendCapExceeded(
                    f"estimated ${est} > per-call cap ${max_usd_per_call}"
                )
            if state["spent"] + est > max_usd_total:
                raise SpendCapExceeded(
                    f"would exceed total cap ${max_usd_total} (spent ${state['spent']:.2f})"
                )
            result = fn(*args, mode=mode, **kw)
            state["spent"] += est
            return result

        wrapper.spent = lambda: state["spent"]
        return wrapper

    return deco


# --------------------------------------------------------------------------------------
# 4. Client scaffolds (OpenAI-compatible)
# --------------------------------------------------------------------------------------
def _client():
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("pip install openai  (see requirements.txt)")
    return OpenAI()  # reads OPENAI_API_KEY


def hello(mode: str = "standard") -> str:
    client = _client()
    model = MODEL_ID if mode == "standard" else MODEL_ID
    resp = client.responses.create(
        model=model,
        input="In two sentences, what makes GPT-6 Astra different from GPT-5.6 Sol?",
    )
    return getattr(resp, "output_text", str(resp))


def computer_use_task(goal: str, mode: str = "standard"):
    """Skeleton of an Astra computer-use run.

    The `tools` block below is a PLACEHOLDER shaped like the Responses API agent
    loop. Check OpenAI's current computer-use docs for the real tool name,
    parameters, and the screenshot/observation round-trip before using this.
    """
    client = _client()
    resp = client.responses.create(
        model=MODEL_ID_PRO if mode == "standard" else MODEL_ID_PRO,
        input=goal,
        tools=[{"type": "computer_use_preview"}],  # <-- placeholder, verify in docs
        # You will typically loop: send screenshot -> get action -> execute -> repeat,
        # with a hard human-approval gate before any irreversible action.
    )
    return resp


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="GPT-6 Astra quickstart utilities.")
    ap.add_argument("--estimate", nargs=2, type=int, metavar=("IN", "OUT"),
                    help="estimate cost for IN input tokens and OUT output tokens")
    ap.add_argument("--mode", default="standard", choices=list(PRICING))
    ap.add_argument("--per-day", type=int, default=None,
                    help="with --estimate: also project daily/monthly at N runs/day")
    ap.add_argument("--route", metavar="TASK", help="print which model should handle TASK")
    ap.add_argument("--hello", action="store_true", help="live smoke test (needs API access)")
    args = ap.parse_args()

    if args.estimate:
        c = estimate_cost(args.estimate[0], args.estimate[1], args.mode)
        print(f"[{c['mode']}]  in {c['input_tokens']:,} tok -> ${c['input_cost_usd']}"
              f"   out {c['output_tokens']:,} tok -> ${c['output_cost_usd']}")
        print(f"  TOTAL: ${c['total_usd']}  ({c['runs_per_dollar']} runs / $1)")
        if args.per_day:
            m = monthly_projection(c["total_usd"], args.per_day)
            print(f"  @ {m['runs_per_day']} runs/day -> ${m['per_day_usd']}/day  "
                  f"${m['per_month_usd']}/month")
        return

    if args.route:
        print(route(args.route))
        return

    if args.hello:
        print(hello(args.mode))
        return

    ap.print_help()


if __name__ == "__main__":
    main()
