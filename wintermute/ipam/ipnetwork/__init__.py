import netaddr
from datetime import datetime
from wintermute.ipam.keys import ip_network_key
from wintermute.ipam.errors import IPNetworkNotFound, ContainerMustBeNetwork, NetworkCannotHaveAggregates, ImproperNetwork
from wintermute.ipam.utils import ip_network_exists
from wintermute.ipam.config import IP_NETWORK_DB

####### IF NETWORK IS EXACT ON MASK BOUNDARY - YOU CAN CREATE IT EVEN THOUGH IT SHOUKD BE A CONTAINER
####### example you can create 192.168.0.0/24 and it will not update the depth index

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
                    raise 
                    HaveAggregates
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
            IP_NETWORK_DB.zadd('DEPTH', self.db_key, 0)
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
    def delete(self):
        for agg in self.aggregates:
            IP_NETWORK_DB.zincrby('DEPTH', agg, -1)
        self._update_v4_networkset(delete=True)
        for key in self.keys:
            self._delete_key(key)

    @property
    def keys(self):
        return IP_NETWORK_DB.hkeys(self.db_key)

    def _delete_key(self, key):
        success = IP_NETWORK_DB.hdel(self.db_key, key)
        if success:
            return True
        else:
            return False

    @property
    def db_key(self):
        return ip_network_key(self.ip_network)

    def get(self, key):
        return IP_NETWORK_DB.hget(self.db_key, key)

    @property
    def aggregates(self):
        aggregates = netaddr.IPNetwork(self.ip_network)
        #Cant find itself if its a /23 and theres a /24 for example - i think this is why depth was not incremented on a /24 that was part of the same /23
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
