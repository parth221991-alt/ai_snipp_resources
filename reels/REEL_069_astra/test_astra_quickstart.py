"""Minimal checks for the cost calculator, router, and spend-cap guard.

    python test_astra_quickstart.py     # or: pytest test_astra_quickstart.py
"""

from astra_quickstart import (
    estimate_cost, monthly_projection, route, spend_cap,
    SpendCapExceeded, MODEL_ID, CHEAP_MODEL,
)


def test_cost_calculator():
    c = estimate_cost(1_000_000, 1_000_000, "standard")
    assert c["input_cost_usd"] == 10.0
    assert c["output_cost_usd"] == 50.0
    assert c["total_usd"] == 60.0

    # the README's worked example: 200K in + 50K out ~= $4.50 standard
    c2 = estimate_cost(200_000, 50_000, "standard")
    assert abs(c2["total_usd"] - 4.5) < 1e-6

    # fast mode is exactly 2x standard
    f = estimate_cost(200_000, 50_000, "fast")
    assert abs(f["total_usd"] - 9.0) < 1e-6


def test_monthly_projection():
    m = monthly_projection(4.5, 100)
    assert m["per_day_usd"] == 450.0
    assert m["per_month_usd"] == 13500.0


def test_router():
    assert route("plan the migration and decide the rollout order") == MODEL_ID
    assert route("navigate to the dashboard and download the report") == MODEL_ID
    assert route("uppercase this string") == CHEAP_MODEL
    assert route("extract the invoice date") == CHEAP_MODEL


def test_spend_cap():
    @spend_cap(max_usd_per_call=5.0, max_usd_total=8.0)
    def call(mode="standard"):
        return "ok"

    # under caps -> fine
    assert call(est_input_tokens=200_000, est_output_tokens=50_000) == "ok"  # ~$4.50

    # second identical call pushes total over $8 -> blocked
    try:
        call(est_input_tokens=200_000, est_output_tokens=50_000)
        assert False, "expected SpendCapExceeded on total cap"
    except SpendCapExceeded:
        pass

    # single oversized call -> blocked by per-call cap
    try:
        call(est_input_tokens=1_000_000, est_output_tokens=1_000_000)  # $60
        assert False, "expected SpendCapExceeded on per-call cap"
    except SpendCapExceeded:
        pass


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS  {name}")
    print("all checks passed")
