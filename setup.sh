OS="$(uname -s)"

# Setup the application from source with a virtual environment
if [ "$OS" = "Linux" ]; then
    # Install dependencies
    sudo apt install libpcap-dev

    # Install virtualenv to the current user if not already installed
    pip3 install virtualenv --user

    # Create the virtualenv and install dependencies locally
    virtualenv -p python3 venv
    source venv/bin/activate 
    pip3 install -r requirements.txt
else
    brew install libpcap
    echo "Non-linux based operating systems aren't supported yet, sorry :("
fi

