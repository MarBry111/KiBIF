
from scapy.all import * # Packet manipulation
from scapy.utils import PcapWriter
import binascii # Binary to Ascii 




num_of_packets_to_sniff = 1000
pcap = sniff( count =num_of_packets_to_sniff, filter='tcp[13] = 2' )
# rdpcap returns packet list
## packetlist object can be enumerated 
print(type(pcap))
print(len(pcap))
print(pcap)
pcap[0]


#pcap =  rdpcap("suspicious.pcap")
#print(pcap)
pktdump = PcapWriter("data_apped.pcap", append=True, sync=True)
pktdump.write(pcap)
#wrpcap("done.pcap",pcap)