                                                  # Changing MAC address of kali machine


import subprocess
import optparse
import re


def search(interface):
    ifconfig_result = subprocess.check_output(['ifconfig', interface])

    mac_address = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address:
        return mac_address.group(0)
    else:
        print("[-] Mac not found")


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option('-i', '--interface', dest="interface", help='Changing mac address of Interface')
    parser.add_option('-m', '--mac', dest="mac", help='Changing mac address')
    return parser.parse_args()

def change_fun(interface, mac):
    print('[..] Changing {} to new mac address {}'.format(interface,mac))
    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', mac])
    subprocess.call(['ifconfig', interface, 'up'])


(option, arguments) = get_arguments()
current_mac = search(option.interface)
print(">> Current mac address of {1} is {0}".format(current_mac,option.interface))
change_fun(option.interface, option.mac)


current_mac = search(option.interface)
if option.mac == current_mac:
    print("[+] Mac address changed successfully \n>> New mac address of {} is {}".format(option.interface, current_mac))
else:
    print("[-] Mac address did'nt changed")