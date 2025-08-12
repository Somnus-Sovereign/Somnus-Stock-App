# Sovereign Local Quant (SLQ) Research Copilot

This project is a local-first, AI-augmented toolkit for quantitative financial research. It is designed to be a **decision-support copilot**, not a fully automated trading system.

For a complete project blueprint, architecture, and development roadmap, please see `Project_Directory.md`.

## Quickstart

1. **Setup the Environment**

    Ensure you have Python 3.9+ installed. Then, run the setup script:

    ```bash
    bash setup.sh
    ```

2. **Activate the Virtual Environment**

    ```bash
    source .venv/bin/activate
    ```

3. **Configure Secrets**

    Copy the example `.env` file and add your API keys.

    ```bash
    cp secrets/.env.example secrets/.env
    # Now edit secrets/.env with your keys
    ```

4. **Run the CLI**

    You can now use the command-line interface to run different parts of the system.

    ```bash
    python cli.py --help
    python cli.py ingest --symbols AAPL,MSFT
    python cli.py research "Test a moving average crossover strategy on tech stocks."
    ```
