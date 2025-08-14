# Utilities

The `utils` module contains a collection of utility functions that are used throughout the project.

## Logger

The `src/utils/logger.py` script provides a structured JSON logger that is used to create an audit trail of all the actions that are taken by the system. This is important for reproducibility, as it allows you to go back and see exactly what the system was doing at any given point in time.

## Config Loader

The `src/utils/config_loader.py` script is responsible for loading the configuration from the `config.py` file and validating its schema. This helps to ensure that the configuration is always valid and that the system is always in a consistent state.
