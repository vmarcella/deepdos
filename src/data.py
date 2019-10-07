"""
    Handle all data operations within the codebase
"""
import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.conf import LATEST_STABLE_MODEL, ROOT_DIR


def load_dataframe(
    csv_location: str = "{ROOT_DIR}/ddos_balanced/final_dataset.csv"
) -> pd.DataFrame:
    """
        Load up our dataframes that contain 100k of each ddos and benign packets

        Returns:
            A dataframe that contains 100k samples of both
    """

    # If we're not reading our large db file, that means we're reading
    # in a generated flow file.
    if csv_location != "{ROOT_DIR}/ddos_balanced/final_dataset.csv":
        input_df = pd.read_csv(csv_location)
        return input_df

    # Load the ddos dataframe
    ddos_df = pd.read_csv(csv_location, nrows=100000, index_col=0)

    features = ddos_df.columns

    # Load the benign dataframe
    benign_df = pd.read_csv(csv_location, nrows=100000, index_col=0, skiprows=6500000)
    benign_df.columns = features

    df = pd.concat([ddos_df, benign_df])
    return df


def load_model(
    has_model: bool = True, model_path: str = f"{LATEST_STABLE_MODEL}"
) -> LogisticRegression:
    """
        Load or create the logistic regression model.

        Returns:
            A logistic regression model either created from scratch or
            loaded from a pickle file
    """
    # Load the model from memory or from a beautiful pickle file
    if has_model:
        lr_file = open(f"{ROOT_DIR}/models/{model_path}", "rb")
        model = pickle.load(lr_file)
        lr_file.close()
    else:
        lr_file = open(f"{ROOT_DIR}/models/{model_path}", "wb")
        model = create_lr()
        pickle.dump(model, lr_file)
        lr_file.close()

    return model


def parse_flow_data(path: str = f"{ROOT_DIR}/flow_output/out.pcap_Flow.csv"):
    """
        Parse the model data
    """
    # Load the df from memory
    print(" - Converting csv into dataframe")
    df = load_dataframe(path)

    # Split up the dataframe
    from_ip = df["Src IP"]
    to_ip = df["Dst IP"]
    protocol = df["Protocol"]
    from_port = df["Src Port"]
    to_port = df["Dst Port"]

    # Clean up the dataframe and create training testing data
    print(" - Cleaning dataframe and obtaining data")
    preprocess_df(df)
    x_train, x_test, _, _ = get_train_test(df)
    data = np.concatenate((x_test, x_train))

    # Create metadata dataframe for use in the main loop
    metadata = pd.DataFrame()
    metadata["from_ip"] = from_ip
    metadata["to_ip"] = to_ip
    metadata["protocol"] = protocol
    metadata["from_port"] = from_port
    metadata["to_port"] = to_port

    return {"data": data, "metadata": metadata}


def preprocess_df(df: pd.DataFrame) -> None:
    """
        Preprocess the dataframe for erraneous/irrelevant columns (In place)

        Args:
            df: The ddos dataframe to be processed

        Returns:
            Nothing
    """
    df.drop(
        ["Flow ID", "Timestamp", "Src IP", "Dst IP", "Flow Byts/s", "Flow Pkts/s"],
        inplace=True,
        axis=1,
    )

    df["Label"] = df["Label"].apply(lambda x: 1 if x == "ddos" else 0)

    for row in df.columns:
        df[row] = np.nan_to_num(df[row])


def get_train_test(df: pd.DataFrame) -> tuple:
    """
        Obtain the training and testing data.

        Returns:
            a tuple containing the training features, testing features,
            training target, and testing target

    """
    x_data = []
    y_data = []

    # Separate features from the target
    for row in df.values:
        x_data.append(row[:-1])
        y_data.append(row[-1])

    X_train, X_test, Y_train, Y_test = train_test_split(x_data, y_data, random_state=1)
    return np.array(X_train), np.array(X_test), np.array(Y_train), np.array(Y_test)


def compute_logistic_model(X_train, X_test, Y_train, Y_test) -> LogisticRegression:
    """
        Create our logistic regression model
    """
    # Obtain a logistic regression
    lr = LogisticRegression()
    lr.fit(X_train, Y_train)
    print(f"Sklearn accuracy: {accuracy_score(lr.predict(X_test), Y_test)}")
    return lr


def create_lr() -> LogisticRegression:
    """
        Create a logistic regression given our base dataframe
    """
    df: pd.DataFrame = load_dataframe()
    preprocess_df(df)
    X_train, X_test, Y_train, Y_test = get_train_test(df)

    return compute_logistic_model(X_train, X_test, Y_train, Y_test)


if __name__ == "__main__":
    df: pd.DataFrame = load_dataframe()
    preprocess_df(df)
    X_train, X_test, Y_train, Y_test = get_train_test(df)
