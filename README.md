# Financial News Sentiment — FNSPID Project

Project for analyzing financial news headlines and correlating sentiment with stock movements.

Goals
- Perform sentiment analysis on `headline` text
- Correlate sentiment with stock price movements around publication date
- Produce actionable recommendations and simple investment strategies

Quickstart
1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the Task 1 EDA script (example):

```bash
python scripts/run_eda.py --input data/raw_analyst_ratings.csv
```

3. Open the Task 1 EDA notebook (if present):

```bash
jupyter notebook notebooks/eda.ipynb
```

4. Open the Task 2 technical indicator analysis notebook:

```bash
jupyter notebook notebooks/task2_analysis.ipynb
```

5. Open the Task 3 sentiment–return correlation notebook (branch `task-3-correlation`):

```bash
jupyter notebook notebooks/task3_correlation.ipynb
```

Repository structure
```
financial_news_sentiment/
├── .vscode/
├── .github/
│   └── workflows/
├── .gitignore
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   ├── data_processing.py          # Task 1 – basic EDA utilities
│   ├── stock_data.py               # Task 2 – price loading helpers
│   ├── financial_analysis.py       # Task 2 – TA indicators & metrics
│   └── sentiment_analysis.py       # Task 3 – VADER sentiment utilities
├── notebooks/
│   ├── eda.ipynb                   # Task 1 – exploratory analysis
│   ├── task2_analysis.ipynb        # Task 2 – TA indicators & metrics
│   └── task3_correlation.ipynb     # Task 3 – sentiment vs return
├── tests/
│   └── test_basic.py
└── scripts/
        └── run_eda.py

## Task overview

### Task 1 – Exploratory Data Analysis (EDA)

- Code: `src/data_processing.py`
- Notebook: `notebooks/eda.ipynb`
- Focus: loading `raw_analyst_ratings.csv`, profiling publishers, headline lengths, time-of-day patterns, and common keywords.

### Task 2 – Technical Indicators & Risk Metrics

- Code:
    - `src/stock_data.py` – helpers to load local CSVs and fetch prices from Yahoo Finance.
    - `src/financial_analysis.py` – technical indicators and portfolio metrics.
- Notebook: `notebooks/task2_analysis.ipynb`.
- Indicators (per ticker):
    - `SMA_20` – 20‑day simple moving average of the close.
    - `RSI_14` – 14‑day Relative Strength Index.
    - `MACD`, `MACD_signal`, `MACD_hist` – standard MACD configuration (12/26/9).
- Metrics (per ticker):
    - Annualised volatility of daily returns.
    - Cumulative return over the full history.
    - Maximum drawdown relative to the running peak.

### Task 3 – News Sentiment vs Stock Returns

- Code: `src/sentiment_analysis.py`.
- Notebook: `notebooks/task3_correlation.ipynb` (developed on branch `task-3-correlation`).
- Sentiment:
    - Uses VADER (`SentimentIntensityAnalyzer`) on each news `headline`.
    - Adds a `sentiment_score` (compound, −1 to 1) per row.
    - Aggregates to average daily sentiment per `(date, stock)`.
- Returns & correlation:
    - Loads the same ticker CSVs as Task 2 and computes daily percentage returns.
    - Aligns sentiment and returns by date and computes Pearson correlations per ticker, with scatter plots for visual inspection.
```

Next steps
- Add CI and daily data ingestion
- Experiment with alternative sentiment models (e.g. transformers)
- Extend the time-series correlation pipeline to multi-day lags and simple trading rules

