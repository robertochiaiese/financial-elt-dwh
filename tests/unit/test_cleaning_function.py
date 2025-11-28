import pandas as pd

def test_column_normalization():
    df = pd.DataFrame({"Open Price": [1], " Close ": [2]})
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    assert list(df.columns) == ["open_price", "close"]
