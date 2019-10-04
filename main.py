"""
    The main functionality of deepdos
"""
import os
import pickle

import numpy

from args import parse_args
from data import (get_train_test, load_dataframe, load_model, parse_flow_data,
                  preprocess_df)
from utils import capture_pcap, execute_cicflowmeter, log_ip_flow


def main_loop():
    """
        Enter the main loop of the program, executing the sub processes
        and executing model commands
    """
    # Init program vars
    predictions = open("predictions.txt", "w+")
    running = True
    model = True

    # load logistic regression model
    model = load_model()

    # Execute the main loop
    while running:
        # Iterate through every pcap captured from my specific ethernet port
        pcap_file = open(f"pcap_info/out.pcap", "w", encoding="ISO-8859-1")
        pcap_list = capture_pcap("wlo1")

        # The counter controls the amount of writes that occur.
        print(f" - Writing packets to out.pcap file")
        pcap_file.writelines(pcap_list)
        pcap_file.close()

        print(" - Writing to csv")
        execute_cicflowmeter()

        # Load model data
        try:
            model_info = parse_flow_data()
        except ValueError:
            print(
                " - Not enough information inside of generated flow, restarting process"
            )
            continue

        # Grab data out of model processor
        data = model_info["data"]
        from_ip = model_info["from_ip"]
        to_ip = model_info["to_ip"]

        # Run model predictions
        result = model.predict(data)
        proba = model.predict_proba(data)

        # Write the status of the connections between IPs
        out_info = zip(from_ip, to_ip, result, proba)
        out_buffer = log_ip_flow(out_info)

        # Write predictions file
        predictions.writelines(line + "\n" for line in out_buffer[0])
        predictions.flush()

        # Remove the old pcap file.
        os.remove("pcap_info/out.pcap")


def start_execution():
    """
        Parse arguments and configure the main loop
    """
    options = parse_args()
    main_loop()


if __name__ == "__main__":
    start_execution()
