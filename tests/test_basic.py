import os
import pandas as pd


def test_pandas_import():
    # simple smoke test
    assert hasattr(pd, "DataFrame")


def test_project_structure_exists():
    base = os.path.dirname(os.path.dirname(__file__))
    assert os.path.exists(base)
