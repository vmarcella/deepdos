import pandas as pd

RM_COLS = ["Flow ID", ""]


def preprocess_chunk(chunk):

    pass


def load_dataframe():
    """
        Load up our dataframes that contain 100k of each ddos and benign packets
    """

    # Load the ddos dataframe
    ddos_df = pd.read_csv(
        "./ddos_balanced/final_dataset.csv", nrows=100000, index_col=0
    )

    features = ddos_df.columns

    # Load the benign dataframe
    benign_df = pd.read_csv(
        "./ddos_balanced/final_dataset.csv", nrows=100000, index_col=0, skiprows=6500000
    )
    benign_df.columns = features

    df = pd.concat([ddos_df, benign_df])
    return df


if __name__ == "__main__":
    df: pd.DataFrame = load_dataframe()
    print(df.columns)
    print(df["Label"].describe())
