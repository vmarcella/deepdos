# deepdos

![PyPI](https://img.shields.io/pypi/v/deepdos)
![PyPI - Downloads](https://img.shields.io/pypi/dm/deepdos)
![Travis (.com)](https://img.shields.io/travis/com/C3NZ/deepdos)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/deepdos)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/deepdos)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/deepdos)
![PyPI - Status](https://img.shields.io/pypi/status/deepdos)
![PyPI - License](https://img.shields.io/pypi/l/deepdos)

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
- [x] Add command line interface

### Long term goals
- [ ] Convert Logistic regression model to a neural network
- [ ] Support both macos and Linux (potentially Windows as well if pcap is easy)
- [ ] Add ddos mitigation/firewall rule support

## How to run/setup

***YOU NEED JAVA INSTALLED IN ORDER FOR DEEPDOS TO RUN THE CICFlowMeter***

### Running from scratch
deepdos is currently only available on linux, but can simply be run by these two commands:
```bash
# clone repo
git clone https://github.com/C3NZ/deepdos

# Install dependencies and setup the projects virtual environment
source bash/setup.sh

# Execute the script (Needs sudo in order to execute both tcpdump and iptables)
python3 main.py -h
```
This will load you into a virtualenv with all of the dependencies installed and ready to use.

To remove all of the dependencies after you're done using the tool, you can simply run:
```bash
source bash/remove.sh
```

and then remove the folder from your computer :)

This will immediately start creating necessary folders, capturing packets, and then identifying
the traffic that is being exchanged in and out of your current computer.


### Installing with pip
#### Linux
```bash
sudo apt install libpcap-dev python3-dev python3-setuptools
pip3 install deepdos

# or deepdos -h, depending on how your path is configured.
python3 -m deepdos -h
```

#### Macos
```bash
brew install libpcap
pip3 install deepdos

# or deepdos -h, depending on how your path is configured.
python3 -m deepdos -h
```
## Usage
```
usage: main.py [-h] [-i INTERFACE] [-n NAUGHTY_COUNT] [--find-interface]
               [--firewall FIREWALL] [--model-type MODEL_TYPE]

Welcome to deepdos, the machine learning/ai based ddos analysis/mitigation
service

optional arguments:
  -h, --help            show this help message and exit
  -i INTERFACE          [REQUIRES SUDO] The network interface for deepdos to
                        listen to (default: None)
  -n NAUGHTY_COUNT      The amount of malicious flows that can come from a
                        given address (default: 10)
  --find-interface      List all of your devices network interfaces. Good if
                        you don't know what interfaces your device has
                        (default: False)
  --firewall FIREWALL   [REQUIRES SUDO] Turn on firewall mode for the given
                        system. linux for Linux systems and macos for mac (Not
                        yet supported) (default: None)
  --model-type MODEL_TYPE
                        The model that you would like to use for classifying
                        the data (default: lr-stable-0.9.0.pickle)
usage: src [-h] [-i INTERFACE] [-n NAUGHTY_COUNT] [--find-interface]
           [--firewall FIREWALL] [--model-type MODEL_TYPE]
```

## Documentation
* [deepdos](./deepdos/docs.md)
* [deepdos.db](./deepdos/db/docs.md)
* [deepdos.args](./deepdos/args/docs.md)
* [deepdos.tests](./deepdos/tests/docs.md)
* [deepdos.analytics](./deepdos/analytics/docs.md)
* [deepdos.firewall](./deepdos/firewall/docs.md)
* [deepdos.utils](./deepdos/utils/docs.md)

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
