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


class NetworkNotAllowedException(Exception):
    pass


class Address(object):
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

    def _allowed_network(self, cidr):
        """
        Determines if the provided network is too large.  If allowed returns
        :class:`netaddr.IPNetwork` object, otherwise raises.

        Currently we are scoping our "allowed" network to a /24.  This is lame
        but the IP allocation algorythim isn't very sophisticated.  Attempting
        to protect against allocating huge contiguous blocks of addresses in
        the DB.

        :param cidr: A string containing the CIDR to validate.
        :raises: :class:`Address.NetworkNotAllowedException` when network
                 is outside the allowed range.
        :raises: :class:`netaddr.AddrFormatError` when invalid cidr.
        """
        ip_network = netaddr.IPNetwork(cidr)
        if ip_network.prefixlen >= 24 and ip_network.prefixlen <= 32:
            return ip_network
        else:
            raise NetworkNotAllowedException

    def ip2int(self, address):
        """
        Convert the given IPv4 address string into an integer.  Returns an
        integer.

        :param address: An IPv4 address string to be converted into an integer.
        """
        return struct.unpack("!I", socket.inet_aton(address))[0]

    def int2ip(self, address_int):
        """
        Convert the given integer into a IPv4 address.  Returns a string.

        :param address_int: An integer to be converted into an IPv4 address.
        """
        return socket.inet_ntoa(struct.pack("!I", address_int))
