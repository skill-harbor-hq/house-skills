# Trade Bot — original design and known results

This reference preserves the design facts of Maxime Proulx's paused NDAX paper-trading prototype. It is the source material the skill explains. It is not a promise that any strategy works, and it does not authorize live trading.

## Identity and status

- **Project:** a local Python paper-trading environment for NDAX crypto markets.
- **Status:** paused. The bot was closed on 2026-09-25 and nothing in this skill restarts it.
- **Money:** no real money. Market prices were real public NDAX prices; orders were simulated in a virtual portfolio.
- **Starting portfolio:** 10,000 CAD.
- **Fees:** NDAX fee model of 0.2% per side, applied to simulated buys and sells.
- **Default symbols:** BTC/CAD and ETH/CAD.
- **Evaluation interval in the live-paper loop:** 60 seconds by default.
- **Credentials:** the paper environment needed no NDAX API key. Its live broker was deliberately not wired.

## Architecture

| Part | Role in the original |
|---|---|
| Configuration | Mode, starting cash, symbols, fee rate, polling interval |
| Market data | Public NDAX prices, tickers, order book and candles through CCXT |
| Paper broker | Virtual cash and positions; executes simulated market buys and sells; writes the trade journal and resumable state |
| Strategy | Receives prices and recent price history, decides whether to buy or sell |
| Live-paper runner | Repeats: read prices, update history, ask the strategy, save state, journal and status |
| Backtest | Replays a strategy over historical candles |
| Live broker guard | A placeholder that kept real trading unwired |

Every simulated trade was journaled with time, symbol, side, quantity, price, fee in CAD, and gross value in CAD.

## Strategy rules shipped as examples

### Mean reversion

- Look back over a 20-price window.
- Buy with a 500 CAD trade size when the price is at least 1% below the window average and enough virtual cash is available.
- Sell the whole position in that symbol when the price is at least 1% above the average.
- The buy and sell percentages are configurable command-line settings.

### Moving-average cross

- Fast average: 10 prices. Slow average: 30 prices.
- Buy with 500 CAD when the fast average crosses from below to above the slow average.
- Sell the whole position when it crosses back below.

### RSI

- Period 14; oversold below 30; overbought above 70.
- Buy with 500 CAD in the oversold zone; sell the whole position in the overbought zone.

### Bollinger Bands

- Window 20, two standard deviations.
- Buy with 500 CAD at or below the lower band; sell the whole position at or above the upper band.

## Backtest convention

The historical replay used candle closes. It approximated both bid and ask with the close, so it ignored the spread, while still applying the 0.2% fee on each side. That makes backtests useful for checking mechanics and comparing rough behaviour, not for proving a real-world return.

## Known test evidence and its limits

- The environment itself was verified end to end with live public NDAX data, a live-paper loop, and forced simulated buy/sell checks.
- **Paper test 1 (2026-09-24):** mean reversion, 120 ticks, BTC/CAD and ETH/CAD. Four simulated trades, 4.00 CAD in fees, final equity 10,010.43 CAD (+0.10%). One short favourable test; it does not establish profitability.
- **Paper test 2 (2026-09-24):** mean reversion, 120 ticks. No trades and final equity 10,000.00 CAD. The market was too flat to trigger the strategy, so that run completed no buy/sell cycle and gives no profitability verdict.
- **Later preserved status (2026-09-25):** a mean-reversion run had reached tick 81 with no trades and a flat 10,000 CAD equity when the project was closed.
- A preserved backtest journal contains 47 simulated fills. The journal records fills, not a complete performance report; do not turn the count into a return claim.

The honest summary is narrow: the machinery ran, journaling worked, one short paper test made four trades and finished slightly up, another made none, and no long or live validation supports a claim that the strategies make money.

## Setting up a user's own paper sandbox

Use the original only as a blueprint. A safe equivalent has:

1. A configuration file that hard-stops the mode at paper.
2. A public-market-data reader that needs no trading credentials.
3. A virtual broker with starting cash, a fee model, positions, state saving, and an append-only or complete trade journal.
4. One strategy at a time behind a small interface that receives prices and history and returns actions.
5. A historical backtest before any live-paper loop.
6. A short fixed-tick paper run, followed by a review of every journaled trade.
7. No live broker, no exchange credential, and no path that can place a real order.

Start with the user's choices for exchange data, symbols, virtual cash, fee assumption, strategy, and thresholds. Write down what will not be tested as clearly as what will.
