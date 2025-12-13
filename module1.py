import pandas as pd

def load_data(path):
    df = pd.read_csv(path, encoding="latin1")
    return df


def preprocess_data(df):
    # Create a delivery delay column
    df["Delivery_Delay"] = df["Days for shipment (scheduled)"] - df["Days for shipping (real)"]

    # Late delivery flag
    df["Is_Late"] = df["Delivery_Delay"] < 0

    return df
