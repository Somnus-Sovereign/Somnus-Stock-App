# Reporting

The `reporting` module is responsible for generating reports that summarize the results of backtesting experiments.

## HTML Reports

The main output of the reporting module is an HTML report that is saved in the `experiments/` directory. This report contains a wealth of information about the performance of the trading strategy, including:

*   An equity curve that shows the growth of the portfolio over time.
*   A table of key performance metrics, such as the Sharpe Ratio, Sortino Ratio, and Maximum Drawdown.
*   A confusion matrix that shows how well the model is able to predict the direction of the market.
*   A feature importance plot that shows which features are most important for the model's predictions.

## TUI Reports

You can also view a summary of the reports in the interactive TUI. The "View Reports" screen shows a list of all the available reports and allows you to view them in the terminal.
