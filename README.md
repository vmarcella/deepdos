# deepdos

## Description
Welcome to deepdos, the python program written to monitor and potentially secure your network
from ddos attacks! While not currently utilizing deep learning to classify packets, deepdos currently
utilizes logistic regression in order to classify packets and has so far been trained on 200,000 packets from
all sorts of DDOS attacks and normal traffic setup. This project couldn't have been
done without the help of the Canadian Institute for Cybersecurity with providing both the original flow dataset 
and tool to create flow csvs from .pcap files. Their site and all resources have been linked at the bottom.


## Goals
### Short term goals
- [ ] Add LR test metrics on startup
- [ ] Update LR to use better data for better performance
- [ ] Add command line interface

### Long term goals
- [ ] Convert Logistic regression model to a neural network
- [ ] Support both macos and Linux (potentially Windows as well if pcap is easy)
- [ ] Add ddos mitigation/firewall rule support

## How to run/setup
deepdos is currently only available on linux, but can simply be run by these two commands:
```bash
# clone repo
git clone https://github.com/C3NZ/deepdos

# install dependencies and allow pcap information to be captured without root.
sudo ./setup.sh

# Install requirements
pip3 install -r requirements.txt

# Execute the script
python3 utils.py
```

This will immediately start creating necessary folders, capturing packets, and then identifying
the traffic that is being exchanged in and out of your current computer.

This also assumes that you have java installed for the program to execute the CICFlowMeter jar
file.

## How to deploy
You can deploy this on your own machine, but production use will come in the future.

## Live deployments
This will be on pypi soon :)

## How to contribute
Fork the current repository and then make the changes that you'd like to said fork. Upon adding features, fixing bugs,
or whatever modifications you've made to the project, issue a pull request to this repository containing the changes that you've made
and I will evaluate them before taking further action. This process may take anywhere from 3-7 days depending on the scope of the changes made, 
my schedule, and any other variable factors.

## Resources
[UNB datasets](https://www.unb.ca/cic/datasets/)

[CICnetflowmeter](http://www.netflowmeter.ca/netflowmeter.html)

[CIC License](CIC_LICENSE.txt)
