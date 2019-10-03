import binascii
import os
import pickle
import subprocess
import time

import numpy
import shortuuid

from data import (compute_logistic_model, create_lr, get_train_test,
                  load_dataframe, preprocess_df)


def capture_pcap(interface: str = "eth0", line_count=1000):
    """
        Capturing pcap information
    """
    # pcap command with tcpdump
    # TODO Enable multiple os commands (Will have to determine the OS)
    pcap_cmd = ["tcpdump", "-i", interface, "-s", "65535", "-w", "-"]
    # Spawn the pcap process
    process = subprocess.Popen(
        pcap_cmd,
        stdout=subprocess.PIPE,
        universal_newlines=False,
        encoding="ISO-8859-1",
    )

    counter = 0
    output_list = []

    # Accrue packets for as long as the line count is.
    # made to be customizable
    while counter < line_count:
        line = process.stdout.readline()
        output_list.append(line)
        counter += 1

    # Close the std output file stream
    process.stdout.close()

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, pcap_cmd)

    return output_list


def execute_cicflowmeter():
    """
        Execute the cicflowmeter to create the flow csv from the pcap file.
    """
    # cic flowmeter command that retrieves all .pcap files from pcap_info and creates
    # a flow output for each .pcap file
    cic_cmd = ["sh", "cfm", "../../../pcap_info", f"../../../flow_output"]

    # Open up the cic flowmeter
    process = subprocess.Popen(
        cic_cmd, cwd="bin/CICFlowMeter-4.0/bin", stdout=subprocess.DEVNULL
    )

    # Wait for the process to be killed
    exit_status = process.wait()

    # If the exit wasn't graceful, throw an error
    if exit_status:
        raise subprocess.CalledProcessError(exit_status, cic_cmd)


def main_loop():
    """
        Enter the main loop of the program, executing the sub processes
        and executing model commands
    """
    # Init program vars
    pcap_file = open(f"pcap_info/out.pcap", "w", encoding="ISO-8859-1")
    predictions = open("predictions.txt", "w+")
    running = True
    model = True

    # Load the model from memory or from a beautiful pickle file
    # TODO fix the logic behind this
    if not model:
        lr_file = open("lr.pickle", "wb")
        lr = create_lr()
        pickle.dump(lr, lr_file)
        lr_file.close()
    else:
        lr_file = open("lr.pickle", "rb")
        lr = pickle.load(lr_file)
        lr_file.close()

    while running:
        # Iterate through every pcap captured from my specific ethernet port
        pcap_list = capture_pcap("wlo1")

        # The counter controls the amount of writes that occur.
        # TODO Enable the counter to be customized via user interaction
        print(f" - Writing packets to out.pcap file")

        pcap_file.writelines(pcap_list)
        pcap_file.close()

        print(" - Writing to csv")
        execute_cicflowmeter()

        # TODO Block into another code chunk
        print(" - Converting csv into dataframe")
        # Load the df and then read from memory
        df = load_dataframe(f"flow_output/out.pcap_Flow.csv")
        from_ip = df["Src IP"]
        to_ip = df["Dst IP"]

        # Preprocess the df for making predictions
        print(" - Cleaning dataframe and obtaining data")
        preprocess_df(df)
        X_train, X_test, Y_train, Y_test = get_train_test(df)
        data = numpy.concatenate((X_test, X_train))

        # Obtaining training results and probabilities
        result = lr.predict(data)
        proba = lr.predict_proba(data)

        # Write the status of the connections between IPs
        out_buffer = []
        out_info = zip(from_ip, to_ip, result, proba)
        for from_ip, to_ip, prediction, proba in out_info:
            src = f"Src IP: {from_ip}"
            dst = f"Dst IP: {to_ip}"
            pred = f"Prediction: {'Malicious' if prediction else 'Safe'}"
            prob = f"Probabilities:"
            safe = f" - Safe - {proba[0] * 100:.2f}%"
            mal = f" - Malicious - {proba[1]*100:.2f}%"

            out_buffer.append(
                ["---IP BLOCK---", src, dst, pred, prob, safe, mal, "--------"]
            )

            # Monolithoc print statement
            # TODO FIX IMMEDIATELY!
            print("---IP---")
            print(src)
            print(dst)
            print(pred)
            print(prob)
            print(safe)
            print(mal)
            print("--------")

        # Write predictions file
        predictions.writelines(line + "\n" for line in out_buffer[0])
        predictions.flush()

        os.remove("pcap_info/out.pcap")
        pcap_file = open(f"pcap_info/out.pcap", "w", encoding="ISO-8859-1")


if __name__ == "__main__":
    main_loop()
