"""Simple runner to execute basic EDA on a CSV file."""
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_processing import load_data, basic_eda
import argparse
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to CSV file with headlines")
    parser.add_argument("--output", required=False, help="Path to write JSON summary")
    args = parser.parse_args()

    df = load_data(args.input)
    summary = basic_eda(df)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        print(f"Wrote summary to {args.output}")
    else:
        print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
