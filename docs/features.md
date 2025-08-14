# Feature Engineering

The `features` module is responsible for generating new features from the raw market data. These features are then used by the machine learning models to make predictions.

## Feature Library

The `src/features/library/` directory contains a collection of hand-crafted, deterministic feature functions. These functions are organized into different modules based on the type of feature they generate. For example, `technical_indicators.py` contains functions for calculating common technical indicators like RSI and moving averages.

## Generated Features

The `src/features/generated/` directory is where the Sovereign Local Model (SLM) saves the feature modules it generates. When you ask the SLM to create a new feature, it will write the Python code for that feature and save it as a new file in this directory.

## Creating New Features

There are two ways to create new features:

1.  **Manually:** You can write a new feature function and add it to one of the modules in the `src/features/library/` directory.
2.  **Using the SLM:** You can ask the SLM to generate the code for a new feature for you. This is the recommended approach, as it allows you to quickly experiment with new ideas without having to write the code yourself.
