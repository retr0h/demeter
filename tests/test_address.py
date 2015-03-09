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

from demeter.address import Address
from demeter.address import NetworkNotAllowedException
from demeter.namespace import Namespace


@ddt
class TestAddress(unittest.TestCase):
    def addr_data():
        ns_name = str(uuid.uuid4())
        cidr = '198.51.100.0/24'
        address = '198.51.100.1'
        address_int = 3325256705
        hostname = 'test-{0}'.format(ns_name)

        return (ns_name, {'cidr': cidr,
                          'address': address,
                          'address_int': address_int,
                          'hostname': hostname})

    def setUp(self):
        self._address = Address()
        self._namespace = Namespace()

    @unpack
    @data(addr_data())
    def test_create_when_namespace_exists(self, ns_name, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name)
        values.update({'namespace': ns})
        addr = self._address.create(**values)

        result = self._address.find_by_ns_and_address(ns_name, address)
        self.assertEquals(address, result.addresses[0].address)

        self._namespace.delete(addr)

    @unpack
    @data(addr_data())
    def test_create_false_when_namespace_not_found(self, ns_name, values):
        values.update({'namespace': None})
        result = self._address.create(**values)
        assert not result

    @unpack
    @data(addr_data())
    def test_delete_cascades(self, ns_name, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name)
        values.update({'namespace': ns})
        addr = self._address.create(**values)
        self._address.delete(addr)

        result = self._address.find_by_ns_and_address(ns_name, address)
        assert not result
        result = self._namespace.find_by_name(ns_name)
        assert not result

    @unpack
    @data(addr_data())
    def test_find_by_ns_and_address(self, ns_name, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name)
        values.update({'namespace': ns})
        addr = self._address.create(**values)

        result = self._address.find_by_ns_and_address(ns_name, address)
        self.assertEquals(address, result.addresses[0].address)

        self._namespace.delete(addr)

    @unpack
    @data(
        (None, '198.51.100.1')
    )
    def test_find_by_ns_and_address_false_when_ns_not_found(self, ns, address):
        result = self._address.find_by_ns_and_address(ns, address)
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
        with self.assertRaises(NetworkNotAllowedException):
            self._address._allowed_network(cidr)

    @data('198.51.100.1')
    def test_ip2int(self, address):
        result = self._address.ip2int(address)
        self.assertEquals(3325256705, result)

    @data(3325256705)
    def test_int2ip(self, addr_int):
        result = self._address.int2ip(addr_int)
        self.assertEquals('198.51.100.1', result)

    # # # # @data(
    # # # #     # (24, 256),
    # # # #     # (25, 128),
    # # # #     # (26, 64),
    # # # #     # (27, 32),
    # # # #     # (28, 16),
    # # # #     # (29, 8),
    # # # #     # (30, 4),
    # # # #     # (31, 2),
    # # # #     (32, 1),
    # # # # )
    # # # # @unpack
    # # # # def test_allocate(self, prefix, expected):
    # # # #     cidr = '192.168.2.0/{0}'.format(prefix)
    # # # #     ns_name = str(ns_name)
    # # # #     self._address.allocate(ns_name, cidr)

    # # # #     # results = self._session.query(Ipv4Address).filter(
    # # # #     #     Ipv4Address.namespace == namespace).all()

    # # # #     # self.assertEquals(expected, len(results))

    # # # # @data(
    # # # #     ('ns-not-found', '198.51.100.0/24')
    # # # # )
    # # # # @unpack
    # # # # def test_allocate_false_when_ns_not_found(self, ns_name, cidr):
    # # # #     result = self._address.allocate(ns_name, cidr)
    # # # #     self.assertEquals(result, False)
