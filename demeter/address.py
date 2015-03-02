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

import netaddr

import demeter
from demeter import models
from demeter import namespace


class NetworkNotAllowedException(Exception):
    pass


class Address(object):
    def create(self, cidr, address, hostname, ns_name):
        ns = namespace.Namespace().find_by_name(ns_name)
        if ns and not self.find_by_ns_and_cidr(ns.name, cidr):
            addr = models.Ipv4Address(cidr=cidr,
                                      address=address,
                                      hostname=hostname,
                                      namespace=ns)
            with demeter.transactional_session() as session:
                session.add(addr)
                return addr

    def delete(self, address):
        with demeter.transactional_session() as session:
            session.delete(address)
            return True

    def find_by_ns_and_cidr(self, ns_name, cidr):
        with demeter.temp_session() as session:
            ns = models.Namespace
            addr = models.Ipv4Address
            return session.query(ns).join(ns.address).filter(
                ns.name == ns_name, addr.cidr == cidr).first()

    def _allowed_network(self, cidr):
        """
        Determines if the provided network is too large.  If allowed returns
        True, otherwise raises.

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
            return True
        else:
            raise NetworkNotAllowedException

    # def allocate(self, namespace, cidr):
    #     """
    #     Populate the database with addresses from the given cidr.  Returns
    #     True on success, otherwise the called functions raise.

    #     TODO: Need to filter the cidr with rules (e.g. network, broadcast,
    #     addresses).

    #     :param namespace: A string containing the namespace to nest the cidr.
    #     :param cidr: A string containing the CIDR to validate.
    #     """
    #     # ip_network = self._valid_network(cidr)
    #     # if ip_network:
    #     #     if self._allowed_network(ip_network):
    #     #         for ip in ip_network:
    #     #             ia = Ipv4Address(namespace=namespace,
    #     #                              cidr=cidr,
    #     #                              address=str(ip))
    #     #             self._session.add(ia)
    #     #         self._session.commit()
    #     #         return True
