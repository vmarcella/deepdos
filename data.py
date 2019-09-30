import ipaddress

import numpy as np
import pandas as pd
from keras.layers.core import Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.model_selection import train_test_split


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


def preprocess_df(df: pd.DataFrame) -> None:
    df.drop(["Flow ID", "Timestamp"], inplace=True, axis=1)

    # Apply a bunch of pre-processing to the columns
    df["Label"] = df["Label"].apply(lambda x: 1 if x == "ddos" else 0)
    df["Src IP"] = df["Src IP"].apply(lambda x: int(ipaddress.IPv4Address(x)))
    df["Dst IP"] = df["Dst IP"].apply(lambda x: int(ipaddress.IPv4Address(x)))
    df["Protocol"] = df.Protocol.astype("category")


def get_train_test(df: pd.DataFrame) -> tuple:
    """
        Obtain the training and testing data.
    """
    X_data = []
    Y_data = []

    for row in df.values:
        X_data.append(row[:-1])
        Y_data.append(row[-1])

    X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, random_state=1)
    return np.array(X_train), np.array(X_test), np.array(Y_train), np.array(Y_test)


if __name__ == "__main__":
    df: pd.DataFrame = load_dataframe()
    preprocess_df(df)
    X_train, Y_test, Y_train, Y_test = get_train_test(df)

    # Create the linear regression model
    model = Sequential()
    model.add(Dense(2, input_dim=81, activation="softmax"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(
        X_train, np_utils.to_categorical(Y_train), epochs=200, batch_size=1, verbose=1
    )
