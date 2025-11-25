import pandas as pd
from typing import Tuple, Dict


def load_data(path: str) -> pd.DataFrame:
    """Load CSV data into a DataFrame.

    Expects columns: headline, url, publisher, date, stock
    """
    df = pd.read_csv(path, parse_dates=["date"], infer_datetime_format=True)
    return df


def basic_eda(df: pd.DataFrame) -> Dict[str, object]:
    """Perform basic EDA and return summary stats.

    Returns a dict with:
    - counts per publisher
    - headline length stats
    - publication time distribution
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
