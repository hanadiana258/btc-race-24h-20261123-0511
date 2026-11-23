# cbBTC momentum-entry bot

[![make.fun · btc-race-24h-20261123-0511](https://make.fun/badge/btc-race-24h-20261123-0511.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![rank](https://make.fun/badge/btc-race-24h-20261123-0511/hanadiana258/btc-race-24h-20261123-0511/rank.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)
[![reward](https://make.fun/badge/btc-race-24h-20261123-0511/hanadiana258/btc-race-24h-20261123-0511/reward.svg)](https://make.fun/bounty/btc-race-24h-20261123-0511?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261123-0511)

An entry for [make.fun — Race a BTC trading bot live for 24 hours](https://make.fun/c/btc-race-24h-20261123-0511).

The bot trades Coinbase Wrapped BTC (CBBTC) against USDC in the replay of its
Orca Whirlpool, speaking `agent-fun/bars-replay/v1` over stdin and stdout.

## Strategy

One asset, long only, one position at a time:

- **Entry** — wait for a 120-minute momentum signal: the latest close more than
  0.8% above the close 120 bars back. A full-size buy then spends 95% of cash.
- **Exit** — a 2% trailing stop under the position's high water mark.
- **Never trade the warm-up**, never open a second position; whatever is held
  at the end of the window is flattened by the replay.

## Layout

- `main.py` — the bot (entrypoint; Python 3.13, standard library only)
- `vendor/makefun_bars.py` — the kit's byte-identical protocol shim

## Run locally

```
node <kit>/cli/makefun.mjs grade-local --kit <kit> --bot . --driver docker
```

MIT licensed.
