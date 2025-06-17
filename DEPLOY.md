# Deployment Guide

This project uses pip for dependency management and pytest/flake8 for development checks.

## Installation

Install all runtime dependencies and test tools:

```bash
pip install -r requirements.txt && pip install pytest flake8
```

## Running Tests

Execute the unit tests and style checks:

```bash
pytest
flake8 .
```

## Launching the Streamlit App

Start the web interface with:

```bash
streamlit run streamlit_app.py
```

## Command-Line Usage

The analysis script can also be run directly:

```bash
python analyze_edf.py <file.edf> [-o OUT_DIR]
```

The optional `-o` argument sets the output directory for the generated CSV and Excel files.
