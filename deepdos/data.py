"""
    Handle all data operations within the codebase
"""
import pickle

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from deepdos.conf import ETC_DIR, LATEST_STABLE_MODEL, ROOT_DIR, create_logger

LOGGER = create_logger(__name__, "INFO")


def load_dataframe(
    csv_location: str = f"{ROOT_DIR}/ddos_balanced/final_dataset.csv"
) -> pd.DataFrame:
    """
        Load up our dataframes that contain 100k of each ddos and benign packets

        Returns:
            A dataframe that contains 100k samples of both
    """

    # If we're not reading our large db file, that means we're reading
    # in a generated flow file.
    if csv_location != f"{ROOT_DIR}/ddos_balanced/final_dataset.csv":
        input_df = pd.read_csv(csv_location)
        return input_df

    # Load the ddos dataframe
    ddos_df = pd.read_csv(csv_location, nrows=100000, index_col=0)

    features = ddos_df.columns

    # Load the benign dataframe
    benign_df = pd.read_csv(csv_location, nrows=100000, index_col=0, skiprows=6500000)
    benign_df.columns = features

    dataframe = pd.concat([ddos_df, benign_df])
    return dataframe


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
        lr_file = open(f"{ETC_DIR}/models/{model_path}", "rb")
        model = pickle.load(lr_file)
        lr_file.close()
        LOGGER.info(f"Loaded model: {model_path}")
    else:
        lr_file = open(f"{ETC_DIR}/models/{model_path}", "wb")
        model = create_lr()
        pickle.dump(model, lr_file)
        lr_file.close()
        LOGGER.info(f"Created and saved: {model_path}")

    return model


def parse_flow_data(path: str = f"{ETC_DIR}/flow_output/out.pcap_Flow.csv"):
    """
        Parse the model data

        Args:
            path - The path to the generated flow data csv file.

        Returns:
            A dictionary containing the model input data and then the metadata about
            the parsed data
    """
    # Load the df from memory

    LOGGER.info("Converting CSV into dataframes")
    dataframe = load_dataframe(path)
    metadata = pd.DataFrame()

    # Setup metadata dataframe through the overall dataframe
    metadata["from_ip"] = dataframe["Src IP"]
    metadata["to_ip"] = dataframe["Dst IP"]
    metadata["protocol"] = dataframe["Protocol"]
    metadata["from_port"] = dataframe["Src Port"]
    metadata["to_port"] = dataframe["Dst Port"]

    # Clean up the dataframe and create training testing data
    LOGGER.info("Cleaning the input dataframe and then getting model input data")
    preprocess_df(dataframe)
    x_train, x_test, _, _ = get_train_test(dataframe)
    data = np.concatenate((x_test, x_train))

    return {"data": data, "metadata": metadata}


def preprocess_df(dataframe: pd.DataFrame) -> None:
    """
        Preprocess the dataframe for erraneous/irrelevant columns (In place)

        Args:
            df: The ddos dataframe to be processed

        Returns:
            Nothing
    """
    dataframe.drop(
        ["Flow ID", "Timestamp", "Src IP", "Dst IP", "Flow Byts/s", "Flow Pkts/s"],
        inplace=True,
        axis=1,
    )

    dataframe["Label"] = dataframe["Label"].apply(lambda x: 1 if x == "ddos" else 0)

    for col in dataframe.columns:
        dataframe[col] = np.nan_to_num(dataframe[col])


def get_train_test(dataframe: pd.DataFrame) -> tuple:
    """
        Obtain the training and testing data.

        Returns:
            a tuple containing the training features, testing features,
            training target, and testing target

    """
    x_data = []
    y_data = []

    # Separate features from the target
    for row in dataframe.values:
        x_data.append(row[:-1])
        y_data.append(row[-1])

    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, random_state=1)
    return np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test)


def compute_logistic_model(x_train, x_test, y_train, y_test) -> LogisticRegression:
    """
        Create our logistic regression model
    """
    # Obtain a logistic regression
    log_reg = LogisticRegression()
    log_reg.fit(x_train, y_train)
    print(f"Sklearn accuracy: {accuracy_score(log_reg.predict(x_test), y_test)}")
    return log_reg


def create_lr() -> LogisticRegression:
    """
        Create a logistic regression given our base dataframe
    """
    dataframe: pd.DataFrame = load_dataframe()
    preprocess_df(dataframe)
    x_train, x_test, y_train, y_test = get_train_test(dataframe)

    return compute_logistic_model(x_train, x_test, y_train, y_test)
