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


class NetworkNotAllowedException(Exception):
    pass


class Namespace(object):
    def create(self, name, cidr):
        self._allowed_cidr(cidr)
        if not self.find_by_name(name):
            ns = models.Namespace(name=name, cidr=cidr)
            with demeter.transactional_session() as session:
                session.add(ns)
                return ns

    def delete(self, ns):
        with demeter.transactional_session() as session:
            session.delete(ns)
            return True

    def delete_by_name(self, name):
        result = self.find_by_name(name)
        if result:
            with demeter.transactional_session() as session:
                session.delete(result)
                return True

    def find_by_name(self, name):
        with demeter.temp_session() as session:
            ns = models.Namespace
            return session.query(ns).outerjoin(ns.addresses).filter(
                ns.name == name).first()

    def _allowed_cidr(self, cidr):
        """
        Determines if the provided network is too large.  If allowed returns
        :class:`netaddr.IPNetwork` object, otherwise raises.

        Not sure if I like this here.  Not sure if I like CIDR bound to
        namespace.  Feels like it belongs in the address class, but moved
        here to avoid circular imports, and namespace is the only class to
        use CIDR.

        :param cidr: A string containing the CIDR to validate.
        :raises: :class:`Address.NetworkNotAllowedException` when network
                 is outside the allowed range.
        :raises: :class:`netaddr.AddrFormatError` when invalid cidr.
        """
        ip_network = netaddr.IPNetwork(cidr)
        if ip_network.prefixlen >= 16 and ip_network.prefixlen <= 32:
            return ip_network
        else:
            raise NetworkNotAllowedException
