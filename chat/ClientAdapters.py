import psutil
import socket


class Adapter:
    def __init__(self, *args, **kwargs):
        self.result = psutil.net_if_addrs()
        self.adapters_stats = psutil.net_if_stats()
        self.af_inet = 2  # ipv4=2 ipv6=23 both=0
        self.ips = socket.getaddrinfo(socket.gethostname(), None, self.af_inet, 1, 0)

    def get_all_adapter(self):
        self.nics = {}
        for key in self.result.keys():
            self.adapter = self.result[key]
            for self.snicaddr in self.adapter:
                if self.snicaddr[0].value == 2:
                    self.nics[key] = self.snicaddr[1]
        return self.nics

    def get_all_ips(self):
        self.IP_LIST = ["127.0.0.1"]
        for i in self.ips:
            self.ip = str(i[4][0])
            self.IP_LIST.append(self.ip)
        return self.IP_LIST

    def get_all_connected_adapter(self):
        self.online_adapters = {}
        for adapter_name in self.adapters_stats:
            if self.adapters_stats[adapter_name][0]:
                self.online_adapters[adapter_name] = True
        return self.online_adapters

    def get_all_socket_family(self):
        return [name for name in dir(socket) if name.isupper() and name.startswith('AF_')]


if __name__ == '__main__':
    adapters = Adapter()
    print(adapters.get_all_adapter())
    print(adapters.get_all_ips())
    print(adapters.get_all_connected_adapter())
    print(adapters.get_all_socket_family())
