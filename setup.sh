# Install pcapdev
sudo apt install libpcap-dev
# Create PCAP
sudo groupadd pcap
# add your user to the PCAP group
sudo usermod -a -G pcap $USER
# Change the ownership of tcpdump to be owned by PCAP
sudo chgrp pcap /usr/sbin/tcpdump
# give file capabilities for caputring raw packets and network admin items
sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
# creaate a sym link for tcp dump in the users bin
sudo ln -s /usr/sbin/tcpdump /usr/bin/tcpdump
