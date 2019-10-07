"""
    Global variables
"""
import os

# Get the root directory for deepdos
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Latest stable model
LATEST_STABLE_MODEL = "lr-stable-0.9.0.pickle"


# Load in the folders that don't exist
if not os.path.exists(f"{ROOT_DIR}/logs"):
    FOLDERS = ["logs", "pcap_info", "flow_output"]
    for folder in FOLDERS:
        os.mkdir(f"{ROOT_DIR}/{folder}")
