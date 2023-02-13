import dpkt


with open('T-PDU.pcapng', 'rb') as f:
  contents = f.read()
  pcap = dpkt.pcapng.Reader(f)


print(contents)
