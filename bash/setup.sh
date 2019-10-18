OS="$(uname -s)"

# Setup the application from source with a virtual environment
if [ "$OS" = "Linux" ]; then
    # Install dependencies
    sudo apt install libpcap-dev python3-dev python3-setuptools
else
    # Macos setup coming soon
    brew install libpcap
    echo "Non-linux based operating systems aren't supported yet, sorry :("
fi

# Install virtualenv to the current user if not already installed
pip3 install virtualenv --user

# Create the virtualenv and install dependencies locally
virtualenv -p python3 venv
source "$(pwd)/venv/bin/activate"
pip3 install -r requirements.txt
