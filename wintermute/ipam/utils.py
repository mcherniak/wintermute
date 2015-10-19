from ipam.keys import ip_network_key
from ipam.config import IP_NETWORK_DB


def ip_network_exists(ip_network):
    if IP_NETWORK_DB.exists(ip_network_key(ip_network)):
        return True
    else:
        return False
