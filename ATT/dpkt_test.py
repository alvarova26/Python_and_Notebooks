import dpkt

f = open('T-PDU.pcapng', 'rb')

pcap = dpkt.pcap.Reader(f)

for ts, buf in pcap:
       eth = dpkt.ethernet.Ethernet(buf)

print(eth)
