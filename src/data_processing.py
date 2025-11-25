import pandas as pd
from typing import Tuple, Dict
import re
from collections import Counter

def load_data(path: str) -> pd.DataFrame:
    """Load CSV data into a DataFrame.

    Expects columns: headline, url, publisher, date, stock
    """
    df = pd.read_csv(path, parse_dates=["date"], infer_datetime_format=True)
    return df

def extract_keywords(text_series: pd.Series, top_n: int = 10) -> Dict[str, int]:
    """Extract common keywords from a text series, excluding basic stop words."""
    stop_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or', 'is', 'are', 'was', 'were', 'with', 'by', 'as', 'from', 'that', 'this', 'it', 'be', 'has', 'have'])
    
    all_words = []
    for text in text_series.dropna():
        # Simple tokenization: lowercase and keep only alphanumeric
        words = re.findall(r'\b\w+\b', str(text).lower())
        all_words.extend([w for w in words if w not in stop_words and not w.isdigit()])
    
    return dict(Counter(all_words).most_common(top_n))

def extract_publisher_domains(publisher_series: pd.Series) -> Dict[str, int]:
    """Extract domains if publishers look like email addresses."""
    domains = []
    for pub in publisher_series.dropna():
        match = re.search(r'@([\w.-]+)', str(pub))
        if match:
            domains.append(match.group(1))
    
    if not domains:
        return {"message": "No email-like publishers found"}
    
    return dict(Counter(domains).most_common())

def basic_eda(df: pd.DataFrame) -> Dict[str, object]:
    """Perform basic EDA and return summary stats.

    Returns a dict with:
    - counts per publisher
    - headline length stats
    - publication time distribution
    - common keywords
    - publisher domains (if applicable)
    """
    result = {}
    df = df.copy()
    df["headline_len"] = df["headline"].fillna("").str.len()

    result["num_records"] = len(df)
    result["publisher_counts"] = df["publisher"].value_counts().to_dict()
    result["headline_length_stats"] = df["headline_len"].describe().to_dict()

    # Extract hour and day for time-based analysis
    if pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["hour"] = df["date"].dt.hour
        df["day_of_week"] = df["date"].dt.day_name()
        result["hour_counts"] = df["hour"].value_counts().sort_index().to_dict()
        result["day_counts"] = df["day_of_week"].value_counts().to_dict()

    # Text Analysis (Topic Modeling / Keywords)
    result["common_keywords"] = extract_keywords(df["headline"])

    # Publisher Analysis (Domains)
    result["publisher_domains"] = extract_publisher_domains(df["publisher"])

    return result


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--out", required=False, help="Path to write JSON summary")
    args = parser.parse_args()

    df = load_data(args.input)
    summary = basic_eda(df)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    else:
        print(summary)
