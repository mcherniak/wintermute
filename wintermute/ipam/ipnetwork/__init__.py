import netaddr
from datetime import datetime
from wintermute.ipam.keys import ip_network_key
from wintermute.ipam.errors import IPNetworkNotFound, ContainerMustBeNetwork, NetworkCannotHaveAggregates, ImproperNetwork
from wintermute.ipam.utils import ip_network_exists
from wintermute.ipam.config import IP_NETWORK_DB


class IPNetwork(netaddr.IPNetwork):
    def __init__(self, ip_network, is_container=False, create=False):
        if not create and not ip_network_exists(ip_network):
            raise IPNetworkNotFound
        self._ip_network = ip_network
        netaddr.IPNetwork.__init__(self, ip_network)
        self._address, prefixlen = ip_network.split('/')
        self._prefixlen = int(prefixlen)
        if not ip_network_exists(ip_network):
            if is_container is True:
                if str(self.network) != str(self._address):
                    raise ContainerMustBeNetwork
            elif is_container is False:
                if self.aggregates:
                    raise NetworkCannotHaveAggregates
                if self[0].value + 1 <= self.value <= self[-1].value:
                    raise ImproperNetwork
            self._set('is_container', str(is_container))
            self._set('date_created', datetime.utcnow().isoformat())
            self._update_v4_networkset()
            self._update_depth()

    @property
    def ip_network(self):
        return self._ip_network

    @property
    def is_container(self):
        return self.get('is_container')

    @is_container.setter
    def is_container(self, value):
        self._set('is_container', value)

    def _set(self, key, value):
        if value != self.get(key):
            IP_NETWORK_DB.hset(self.db_key, key, value)
            IP_NETWORK_DB.hset(self.db_key, 'last_updated',
                               datetime.utcnow().isoformat())
        return True

    def _update_depth(self):
        if len(self.supernets) == 0:
            for network in self.aggregates:
                IP_NETWORK_DB.zincrby('DEPTH', network, 1)
        else:
            score = len(self.supernets)
            IP_NETWORK_DB.zadd('DEPTH', self.db_key, score)

    def _update_v4_networkset(self, delete=False):
        score = float('{}.{}'.format(self.value, self._prefixlen))
        if delete:
            IP_NETWORK_DB.zrem('NETWORKSET', self.db_key, score)
            return True
        else:
            print(IP_NETWORK_DB.zadd('NETWORKSET', self.db_key, score))
            return True

    @property
    def db_key(self):
        return ip_network_key(self.ip_network)

    def get(self, key):
        return IP_NETWORK_DB.hget(self.db_key, key)

    @property
    def aggregates(self):
        aggregates = netaddr.IPNetwork(self.ip_network)
        min_score = aggregates[0].value + 1
        max_score = aggregates[-1].value
        return IP_NETWORK_DB.zrangebyscore('NETWORKSET', min_score, max_score)

    @property
    def supernets(self):
        supernets = []
        for supernet in self.supernet():
            if ip_network_exists(supernet):
                supernets.append(supernet)
        return supernets
