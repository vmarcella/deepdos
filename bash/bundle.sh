# Remove all previous distributions
rm dist/*
# Bundle our distribution
python3 setup.py sdist bdist_wheel
# Verify that it's good
twine check dist/*
