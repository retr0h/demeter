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
import netaddr
import unittest2 as unittest

from demeter.namespace import Namespace
from demeter.namespace import NetworkNotAllowedException
from tests import helper


@ddt
class TestNamespace(unittest.TestCase):
    def setUp(self):
        self._namespace = Namespace()

    @unpack
    @data(helper.namespace_data())
    def test_all(self, name, cidr):
        ns = self._namespace.create(name, cidr)

        result = self._namespace.all()
        self.assertEquals(1, len(result))

        self._namespace.delete(ns)

    @unpack
    @data(helper.namespace_data())
    def test_all_is_empty(self, name, cidr):
        result = self._namespace.all()
        self.assertEquals([], result)

    @unpack
    @data(helper.namespace_data())
    def test_create(self, name, cidr):
        ns = self._namespace.create(name, cidr)

        result = self._namespace.find_by_name(name)
        self.assertEquals(name, result.name)

        self._namespace.delete(ns)

    @unpack
    @data(helper.namespace_data(cidr='198.51.100.0/36'))
    def test_create_not_allowed(self, name, cidr):
        with self.assertRaises(netaddr.AddrFormatError):
            self._namespace.create(name, cidr)

    @unpack
    @data(helper.namespace_data())
    def test_delete(self, name, cidr):
        ns = self._namespace.create(name, cidr)

        result = self._namespace.delete(ns)
        assert result
        result = self._namespace.find_by_name(name)
        assert not result

        self._namespace.delete(ns)

    @unpack
    @data(helper.namespace_data())
    def test_delete_by_name(self, name, cidr):
        ns = self._namespace.create(name, cidr)

        result = self._namespace.delete_by_name(name)
        assert result

        self._namespace.delete(ns)

    @data('name-not-found')
    def test_delete_by_name_is_false_when_not_found(self, name):
        result = self._namespace.delete_by_name(name)
        assert not result

    @unpack
    @data(helper.namespace_data())
    def test_find_by_name(self, name, cidr):
        ns = self._namespace.create(name, cidr)

        result = self._namespace.find_by_name(name)
        self.assertEquals(name, result.name)

        self._namespace.delete(ns)

    @data('name-not-found')
    def test_find_by_name_is_false_when_not_found(self, name):
        result = self._namespace.find_by_name(name)
        assert not result

    @data('198.51.100.0/24')
    def test_allowed_cidr(self, cidr):
        result = self._namespace._allowed_cidr(cidr)
        assert result

    @data('198.51.100.0/36')
    def test_allowed_cidr_raises_on_invalid_cidr(self, cidr):
        with self.assertRaises(netaddr.AddrFormatError):
            self._namespace._allowed_cidr(cidr)

    @data('198.51.100.0/15')
    def test_allowed_cidr_raises_on_disallowed(self, cidr):
        with self.assertRaises(NetworkNotAllowedException):
            self._namespace._allowed_cidr(cidr)
