# Financial News Sentiment — FNSPID Project

Project scaffold for analyzing financial news headlines and correlating sentiment with stock movements.

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

2. Run a simple EDA script:

```bash
python scripts/run_eda.py --input data/sample.csv
```

3. Open the EDA notebook:

```bash
jupyter notebook notebooks/eda.ipynb
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
│   └── data_processing.py
├── notebooks/
│   └── eda.ipynb
├── tests/
│   └── test_basic.py
└── scripts/
    └── run_eda.py
```

Next steps
- Add CI and daily data ingestion
- Implement sentiment model (VADER, transformers)
- Build time-series correlation pipeline

