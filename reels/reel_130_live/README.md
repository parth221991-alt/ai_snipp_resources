# Your AI bot crushed the backtest. Then it failed live.

Here you go 👇

NautilusTrader: https://github.com/nautechsystems/nautilus_trader
Install: pip install -U nautilus_trader (add --pre for the 2.0 pre-release, as its README explains)

The 4 checks we run before any bot goes live:
1. Every price in the test actually traded. Look for stale opening ticks, filled-in gaps and zero-volume bars.
2. One code path. The same strategy code produces backtest and live orders.
3. Fills modelled worse than the screen price, especially stop losses.
4. Weeks of paper trading where the bot's trades match the replay trade for trade. If they don't match, find out why before real money.

In India, every API order is an algo order under SEBI's framework, and algo orders can't be market orders. Plan for limit orders that don't fill.

## Sources
Stale tick: 53 recorded days, 12,839 NIFTY option contracts (2026-11-09). Replay fidelity 2026-10-28: ~7% optimistic, stop fills 1.3-2.2 pt worse live. NautilusTrader README + GitHub API 2026-11-12 (31,475 stars, LGPL-3.0, "identical strategy implementations between research and live"). NSE retail algo FAQ 03-11-2025 (Q8, Q11).
