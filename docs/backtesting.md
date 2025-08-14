# Backtesting Engine

The `backtesting` module is responsible for simulating the performance of a trading strategy over a historical period.

## The Backtester

The backtesting engine is located in `src/backtesting/engine.py`. It uses a walk-forward approach to simulate trading. This means that the model is trained on a certain period of data, and then it is used to make predictions on the next period of data. This process is repeated until the end of the historical data is reached.

## Simulated Events

The backtester simulates the following events:

*   **Slippage:** The difference between the expected price of a trade and the price at which the trade is actually executed.
*   **Fees:** The commissions and other fees that are charged by the brokerage.
*   **Borrow Costs:** The cost of borrowing money to make a trade.
*   **Delay:** The delay between when a trade is signaled and when it is executed.
*   **Position Limits:** The maximum amount of money that can be invested in a single position.
*   **Risk Caps:** The maximum amount of risk that can be taken on at any given time.

By simulating these events, the backtester provides a more realistic estimate of how a trading strategy would have performed in the real world.
