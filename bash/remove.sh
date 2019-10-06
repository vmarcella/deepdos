OS="$(uname -s)"


# Setup symbolic links for permissioning important network binaries
if [ $OS = "Linux" ]; then
    # Remove libpcap-dev, as it is not needed anymore
    sudo apt remove libpcap-dev
    
    # Deactivate the virtual environment if it's running
    if [[ "$VIRTUAL_ENV" == "venv" ]]; then
        deactivate
    fi

    # Remove everything from the virtualenv
    rm -r "$(pwd)/venv"
    echo "It is now safe to delete the deepdos folder!"

else
    brew remove libpcap
    echo "Non-linux based operating systems aren't fully supported yet, sorry :("
fi

