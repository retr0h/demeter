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

from ddt import data
from ddt import ddt
from ddt import unpack
import unittest2 as unittest

from demeter.address import Address
from demeter.namespace import Namespace
from tests import helper


@ddt
class TestAddress(unittest.TestCase):
    def setUp(self):
        self._address = Address()
        self._namespace = Namespace()

    @unpack
    @data(helper.address_data())
    def test_create_when_namespace_exists(self, ns_name, cidr, family, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})
        self._address.create(**values)

        result = self._address.find_by_ns_and_address(ns_name, address)
        self.assertEquals(address, result.addresses[0].address)

        self._namespace.delete(ns)

    @unpack
    @data(helper.address_data())
    def test_create_false_when_namespace_not_found(self,
                                                   ns_name,
                                                   cidr,
                                                   family,
                                                   values):
        values.update({'namespace': None})
        result = self._address.create(**values)
        assert not result

    @unpack
    @data(helper.address_data())
    def test_delete_cascades(self, ns_name, cidr, family, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})
        self._address.create(**values)
        self._namespace.delete(ns)

        result = self._address.find_by_ns_and_address(ns_name, address)
        assert not result
        result = self._namespace.find_by_name(ns_name)
        assert not result

    @unpack
    @data(helper.address_data())
    def test_find_by_ns_and_address(self, ns_name, cidr, family, values):
        address = values.get('address')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})
        self._address.create(**values)

        result = self._address.find_by_ns_and_address(ns_name, address)
        self.assertEquals(address, result.addresses[0].address)

        self._namespace.delete(ns)

    @unpack
    @data(
        (None, '198.51.100.1')
    )
    def test_find_by_ns_and_address_false_when_ns_not_found(self, ns, address):
        result = self._address.find_by_ns_and_address(ns, address)
        assert not result

    @unpack
    @data(helper.address_data())
    def test_next(self, ns_name, cidr, family, values):
        hostname = values.get('hostname')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})
        self._address.create(**values)

        result = self._address.next(ns_name, hostname)
        self.assertEquals(3325256706, result.address_int)

        self._namespace.delete(ns)

    @unpack
    @data(helper.address_data())
    def test_next_when_none_used(self, ns_name, cidr, family, values):
        hostname = values.get('hostname')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})

        result = self._address.next(ns_name, hostname)
        self.assertEquals(3325256705, result.address_int)

        self._namespace.delete(ns)

    @unpack
    @data(helper.address_data(cidr='198.51.100.1/32', address='198.51.100.1'))
    def test_next_when_none_free(self, ns_name, cidr, family, values):
        hostname = values.get('hostname')
        ns = self._namespace.create(ns_name, cidr, family)
        values.update({'namespace': ns})

        result = self._address.next(ns_name, hostname)
        assert not result

        self._namespace.delete(ns)

    @data('198.51.100.0/24')
    def test_cidr_list(self, cidr):
        result = self._address._cidr_list(cidr)
        self.assertEquals(254, len(result))
        self.assertEquals(3325256705, result[0])

    @unpack
    @data(([1, 2, 3], [1, 2, 3, 4, 5]))
    def test_compare(self, a, b):
        result = self._address._compare(a, b)
        self.assertEquals(set([4, 5]), result)

    @unpack
    @data(([1, 2, 3], [2, 1, 3]))
    def test_compare_sets_are_equal(self, a, b):
        result = self._address._compare(a, b)
        self.assertEquals(set([]), result)

    @data((1, 2, 3, 4, 5))
    def test_next_in_set(self, s):
        result = self._address._next_in_set(s)
        self.assertEquals(1, result)

    @data(())
    def test_next_in_set_is_empty(self, s):
        result = self._address._next_in_set(s)
        assert not result

    @data('198.51.100.1')
    def test_ip2int(self, address):
        result = self._address._ip2int(address)
        self.assertEquals(3325256705, result)

    @data(3325256705)
    def test_int2ip(self, addr_int):
        result = self._address._int2ip(addr_int)
        self.assertEquals('198.51.100.1', result)
