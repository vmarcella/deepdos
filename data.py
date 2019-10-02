import ipaddress

import numpy as np
import pandas as pd
from keras.layers import LSTM
from keras.layers.core import Dense
from keras.models import Sequential
from keras.utils import np_utils
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def load_dataframe() -> pd.DataFrame:
    """
        Load up our dataframes that contain 100k of each ddos and benign packets

        Returns:
            A dataframe that contains 100k samples of both
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
    """
        Preprocess the dataframe for erraneous/irrelevant columns (In place)

        Args:
            df: The ddos dataframe to be processed

    """
    df.drop(
        ["Flow ID", "Timestamp", "Src IP", "Dst IP", "Flow Byts/s", "Flow Pkts/s"],
        inplace=True,
        axis=1,
    )

    # Apply a bunch of pre-processing to the columns
    df["Label"] = df["Label"].apply(lambda x: 1 if x == "ddos" else 0)
    # df["Src IP"] = df["Src IP"].apply(lambda x: int(ipaddress.IPv4Address(x)))
    # df["Dst IP"] = df["Dst IP"].apply(lambda x: int(ipaddress.IPv4Address(x)))
    # df["Protocol"] = df.Protocol.astype("category")

    for row in df.columns:
        df[row] = np.nan_to_num(df[row])
        print(np.any(np.isnan(df[row])))

    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]


def get_train_test(
    ddos_df: pd.DataFrame
) -> tuple(np.array, np.array, np.array, np.array):
    """
        Obtain the training and testing data.

        Returns:

    """
    x_data = []
    y_data = []

    for row in df.values:
        x_data.append(row[:-1])
        y_data.append(row[-1])

    X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, random_state=1)
    return np.array(X_train), np.array(X_test), np.array(Y_train), np.array(Y_test)


def compute_logistic_model(X_train, X_test, Y_train, Y_test):
    """
        Create our logistic regression model
    """
    # Obtain a logistic regression
    lr = LogisticRegression()
    lr.fit(X_train, Y_train)
    print(f"Sklearn accuracy: {accuracy_score(lr.predict(X_test), Y_test)}")


def compute_neural_network(X_train, X_test, Y_train, Y_test):
    """
        Create our NN model
    """
    # Create a sequential model
    model = Sequential()
    model.add(Dense(12, input_dim=77, activation="sigmoid"))
    model.add(Dense(6, activation="sigmoid"))
    model.add(Dense(2, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(
        X_train, np_utils.to_categorical(Y_train), epochs=200, batch_size=50, verbose=1
    )


if __name__ == "__main__":
    df: pd.DataFrame = load_dataframe()
    preprocess_df(df)
    X_train, X_test, Y_train, Y_test = get_train_test(df)

    compute_logistic_model(X_train, X_test, Y_train, Y_test)
