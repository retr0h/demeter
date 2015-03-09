# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2015 John Dewey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import socket
import struct

import netaddr

import demeter
from demeter import models
from demeter.namespace import Namespace


class Address(object):
    def __init__(self):
        self._namespace = Namespace()

    def create(self, **kwargs):
        namespace = kwargs.get('namespace')
        address = kwargs.get('address')
        if namespace:
            ns_name = namespace.name
            if not self.find_by_ns_and_address(ns_name, address):
                addr = models.Ipv4Address(**kwargs)
                with demeter.transactional_session() as session:
                    session.add(addr)
                    return addr

    def delete(self, address):
        with demeter.transactional_session() as session:
            session.delete(address)
            return True

    def find_by_ns_and_address(self, ns_name, address):
        with demeter.temp_session() as session:
            ns = models.Namespace
            addr = models.Ipv4Address
            return session.query(ns).join(ns.addresses).filter(
                ns.name == ns_name, addr.address == address).first()

    def next(self, ns_name, hostname):
        ns = self._namespace.find_by_name(ns_name)
        if ns:
            cidr = ns.cidr
            allocated_address_list = [int(a.address_int)
                                      for a in ns.addresses]
            available_address_set = self._compare(self._cidr_list(cidr),
                                                  allocated_address_list)
            if available_address_set:
                address_int = self._next_in_set(available_address_set)
                address = self._int2ip(address_int)
                return self.create(address=address,
                                   address_int=address_int,
                                   hostname=hostname,
                                   namespace=ns)

    def _cidr_list(self, cidr):
        """
        Construct a list of integers from an IPv4 cidr.  Returns a list.

        :param cidr: A string containing the CIDR to validate.
        """
        ip_network = netaddr.IPNetwork(cidr)
        return [self._ip2int(str(ip)) for ip in ip_network if
                not (ip == ip_network.network or ip == ip_network.broadcast)]

    def _compare(self, a, b):
        return (set(a) ^ set(b))

    def _next_in_set(self, s):
        try:
            return next(iter(s))
        except StopIteration:
            return None

    def _ip2int(self, address):
        """
        Convert the given IPv4 address string into an integer.  Returns an
        integer.

        :param address: An IPv4 address string to be converted into an integer.
        """
        return struct.unpack("!I", socket.inet_aton(address))[0]

    def _int2ip(self, address_int):
        """
        Convert the given integer into a IPv4 address.  Returns a string.

        :param address_int: An integer to be converted into an IPv4 address.
        """
        return socket.inet_ntoa(struct.pack("!I", address_int))
