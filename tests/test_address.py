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

import uuid

from ddt import data
from ddt import ddt
from ddt import unpack
import netaddr
import unittest2 as unittest

from demeter import Address
from demeter import Namespace


@ddt
class TestAddress(unittest.TestCase):
    def setUp(self):
        self._address = Address.Address()
        self._namespace = Namespace.Namespace()

    @unpack
    @data(
        (str(uuid.uuid4()), '198.51.100.0/24', '198.51.100.1', 'test-hostname')
    )
    def test_create_when_namespace_exists(self,
                                          ns_name,
                                          cidr,
                                          address,
                                          hostname):
        self._namespace.create(ns_name)
        addr = self._address.create(cidr, address, hostname, ns_name)

        result = self._address.find_by_ns_and_cidr(ns_name, cidr)
        self.assertEquals(cidr, result.address.cidr)

        self._namespace.delete(addr)

    @unpack
    @data(
        ('ns-not-found', '198.51.100.0/24', '198.51.100.1', 'invalid-hostname')
    )
    def test_create_is_false_when_namespace_not_found(self,
                                                      ns_name,
                                                      cidr,
                                                      address,
                                                      hostname):
        result = self._address.create(cidr, address, hostname, ns_name)
        assert not result

    @unpack
    @data(
        (str(uuid.uuid4()), '198.51.100.0/24', '198.51.100.1', 'test-hostname')
    )
    def test_delete_cascades(self, ns_name, cidr, address, hostname):
        self._namespace.create(ns_name)
        addr = self._address.create(cidr, address, hostname, ns_name)
        self._address.delete(addr)

        result = self._address.find_by_ns_and_cidr(ns_name, cidr)
        assert not result
        result = self._namespace.find_by_name(ns_name)
        assert not result

    @unpack
    @data(
        (str(uuid.uuid4()), '198.51.100.0/24', '198.51.100.1', 'test-hostname')
    )
    def test_find_by_ns_and_cidr(self, ns_name, cidr, address, hostname):
        self._namespace.create(ns_name)
        addr = self._address.create(cidr, address, hostname, ns_name)

        result = self._address.find_by_ns_and_cidr(ns_name, cidr)
        self.assertEquals(cidr, result.address.cidr)

        self._namespace.delete(addr)

    @unpack
    @data(
        ('ns-not-found', '198.51.100.0/24')
    )
    def test_find_by_ns_and_cidr_is_false_when_not_found(self, ns_name, cidr):
        result = self._address.find_by_ns_and_cidr(ns_name, cidr)
        assert not result

    @data('198.51.100.0/24')
    def test_allowed_network(self, cidr):
        result = self._address._allowed_network(cidr)
        assert result

    @data('198.51.100.0/36')
    def test_allowed_network_raises_on_invalid_cidr(self, cidr):
        with self.assertRaises(netaddr.AddrFormatError):
            self._address._allowed_network(cidr)

    @data('198.51.100.0/22')
    def test_allowed_network_raises_on_disallowed(self, cidr):
        with self.assertRaises(Address.NetworkNotAllowedException):
            self._address._allowed_network(cidr)

    # # @data(
    # #     (24, 256),
    # #     (25, 128),
    # #     (26, 64),
    # #     (27, 32),
    # #     (28, 16),
    # #     (29, 8),
    # #     (30, 4),
    # #     (31, 2),
    # #     (32, 1),
    # # )
    # # @unpack
    # # def test_allocate(self, value, expected):
    # #     cidr = '192.168.2.0/{0}'.format(value)
    # #     namespace = 'test_namespace_{0}'.format(value)
    # #     self._address.allocate(namespace, cidr)

    # #     results = self._session.query(Ipv4Address).filter(
    # #         Ipv4Address.namespace == namespace).all()

    # #     self.assertEquals(expected, len(results))
