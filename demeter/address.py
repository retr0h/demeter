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
import sqlalchemy.orm as orm

from demeter import client
from demeter.models import Ipv4Address


class InvalidNetworkException(Exception):
    pass


class NetworkNotAllowedException(Exception):
    pass


class Address(object):
    def __init__(self):
        engine = client.get_engine()
        Session = orm.sessionmaker(bind=engine)
        self._session = Session()

    def _valid_network(self, cidr):
        """
        Determines if the given CIDR is valid.  If valid returns a
        :class:`netaddr.IPNetwork` object, otherwise raises.

        :param cidr: A string containing the CIDR to validate.
        :raises: :class:`Address.InvalidNetworkException` when invalid cidr.
        """
        try:
            return netaddr.IPNetwork(cidr)
        except netaddr.AddrFormatError:
            raise InvalidNetworkException

    def _allowed_network(self, ip_network):
        """
        Determines if the provided network is too large.  If allowed returns
        True, otherwise raises.

        Currently we are scoping our "allowed" network to a /24.  This is lame
        but the IP allocation algorythim isn't very sophisticated.  Attempting
        to protect against allocating huge contiguous blocks of addresses in
        the DB.

        :param ip_network: A :class:`netaddr.IPNetwork` object.
        :raises: :class:`Address.NetworkNotAllowedException` when network
                 is outside the allowed range.
        """
        if ip_network.prefixlen >= 24 and ip_network.prefixlen <= 32:
            return True
        else:
            raise NetworkNotAllowedException

    def allocate(self, pool_name, cidr):
        """
        Populate the database with addresses from the given cidr.  Returns True
        on success, otherwise the called functions raise.

        TODO: Need to filter the cidr with rules (e.g. network, broadcast,
        addresses).

        :param pool_name: A string containing the name to call the cidr.
        :param cidr: A string containing the CIDR to validate.
        """
        ip_network = self._valid_network(cidr)
        if ip_network:
            if self._allowed_network(ip_network):
                for ip in ip_network:
                    ia = Ipv4Address(pool_name=pool_name,
                                     pool_cidr=cidr,
                                     address=str(ip))
                    self._session.add(ia)
                self._session.commit()
                return True
