#!/usr/bin/env python3
"""cbBTC momentum-entry bot for the make.fun bars replay.

Trades one asset, CBBTC, long only, one position at a time. The entry is a
120-minute momentum signal, the exit a 2 percent trailing stop under the
position's high water mark. The replay flattens whatever is still held at
the last close of the window.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))

import makefun_bars as bars

SYMBOL = "CBBTC"
MOMENTUM_BARS = 120
ENTRY_GAP = 0.008       # the 120-bar return a buy needs
TRAIL_STOP = 0.02       # trailing stop under the high water mark
BUY_FRACTION = 0.95     # share of cash a buy spends
SLIPPAGE_BPS = 10_000   # slippage left open: the stop bounds the risk

closes = []             # every close seen so far, latest last
high_water = None       # the position's high water mark


def on_batch(state, batch):
    """Answer one batch with at most one order: a full-size buy or the stop's sell."""
    global high_water
    price = state.close(SYMBOL)
    if price is None:
        return []
    closes.append(price)
    held = state.positions.get(SYMBOL)
    if held is None:
        if state.warming_up or len(closes) <= MOMENTUM_BARS:
            return []
        past = closes[-1 - MOMENTUM_BARS]
        if price / past - 1.0 < ENTRY_GAP:
            return []
        high_water = price
        # 95 percent of cash: nearly full exposure, a little headroom so the
        # buy never races the weight cap. The trailing stop, not a slippage cap,
        # bounds the downside.
        spend = int(state.cash * BUY_FRACTION)
        min_notional = int(state.hello["fees"]["min_notional_quote_units"])
        if spend < min_notional:
            return []
        return [{"side": "buy", "symbol": SYMBOL, "notional_quote_units": spend,
                 "max_slippage_bps": SLIPPAGE_BPS}]
    high_water = max(high_water or price, price)
    if price >= high_water * (1.0 - TRAIL_STOP):
        return []
    return [{"side": "sell", "symbol": SYMBOL, "qty": held.qty,
             "max_slippage_bps": SLIPPAGE_BPS}]


if __name__ == "__main__":
    bars.run(on_batch)
