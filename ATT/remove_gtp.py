### NOT WORKING - NEEDS A REVIEW
# How to run it:
# > python sample.py Hello Python 
# > sys.argv[0] == ‘sample.py’ 
# > sys.argv[1] == ‘Hello’ 
# > sys.argv[2] == ‘Python’

# Getting error:
# (base) C:\Users\alvaro.mendoza\Documents\GitHub\Python_and_Notebooks\ATT>python remove_gtp.py input.pcap output.pcap
# Traceback (most recent call last):
#   File "C:\Users\alvaro.mendoza\Documents\GitHub\Python_and_Notebooks\ATT\remove_gtp.py", line 26, in <module>
#     pcapin = dpkt.pcap.Reader(fi)
#   File "C:\Users\alvaro.mendoza\Anaconda3\lib\site-packages\dpkt\pcap.py", line 318, in __init__
#     buf = self.__f.read(FileHdr.__hdr_len__)
#   File "C:\Users\alvaro.mendoza\Anaconda3\lib\encodings\cp1252.py", line 23, in decode
#     return codecs.charmap_decode(input,self.errors,decoding_table)[0]
# UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 436: character maps to <undefined>


'''Remove GTP layer from PCAP file'''
import dpkt, struct, time, re, socket
import platform
import sys

# Check for arguments
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print("Usage:\n", sys.argv[0], "input.pcap", "output.pcap")
    sys.exit()

# Open files for input and output
try:
    fi = open(sys.argv[1], 'r')
    fo = open(sys.argv[2], 'w')
    print('1')
    # Prepare PCAP reader and writter
    pcapin = dpkt.pcap.Reader(fi)
    print('2')
    pcapout = dpkt.pcap.Writer(fo)

    for ts, buf in pcapin:
        # make sure we are dealing with IP traffic
        # ref: http://www.iana.org/assignments/ethernet-numbers
        try: eth = dpkt.ethernet.Ethernet(buf)
        except: continue
        if eth.type != 2048: continue

        # make sure we are dealing with UDP
        # ref: http://www.iana.org/assignments/protocol-numbers/
        try: ip = eth.data
        except: continue
        if ip.p != 17: continue

        # filter on UDP assigned ports for GTP User
        # ref: http://www.iana.org/assignments/port-numbers
        try: udp = ip.data
        except: continue
        try:
            if udp.dport != 2152: continue
        except: continue

        # extract GTP flags to detect header length
        gtpflags = udp.data[:1]
        try:
            if gtpflags == '\x30': payload = udp.data[8:]
            elif gtpflags == '\x32': payload = udp.data[12:]
            else: continue
        except: continue

        # at this point we have a confirmed ETH/IP/UDP/GTP packet structure
        # UDP payload is GTP header + real user payload
        try:
            # append real user payload to ethernet layer and writeout
            eth.data = payload
            pcapout.writepkt(eth, ts)
        except: continue

    fi.close()
    fo.close()

except IOError as e:
   errno, strerror = e.args
   print ("I/O error({0}): {1}".format(errno, strerror))

#except IOError as (errno, strerror):
#    print ("I/O error({0}): {1}".format(errno, strerror))
