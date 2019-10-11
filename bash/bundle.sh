# Remove all previous distributions
rm dist/*
rm -rf deepdos/.etc/external/bin/logs
rm -rf deepdos/.etc/logs
sudo rm -rf deepdos/.etc/pcap_info
sudo rm -rf deepdos/.etc/flow_output

# Bundle our distribution
python3 setup.py sdist bdist_wheel

# Verify that it's good
twine check dist/*
