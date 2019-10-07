# Remove all previous distributions
rm dist/*
rm -rf deepdos/external/bin/logs
rm -rf deepdos/logs
rm -rf deepdos/pcap_info
rm -rf deepdos/flow_output

# Bundle our distribution
python3 setup.py sdist bdist_wheel --owner=root --group=root

# Verify that it's good
twine check dist/*
