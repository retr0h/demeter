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

from demeter import Address
from demeter import Namespace


@ddt
class TestNamespace(unittest.TestCase):
    def setUp(self):
        self._address = Address.Address()
        self._namespace = Namespace.Namespace()
        self._namespace.delete_all()

    @data('test-namespace')
    def test_create(self, name):
        self._namespace.create(name)

        result = self._namespace.find_by_name(name)
        self.assertEquals('test-namespace', result.name)

    @unpack
    @data(
        ('test-namespace', 'test-parentless', '198.51.100.0/24',
         '198.51.100.1', 'test-hostname')
    )
    # @data('test-namespace')
    def test_delete_all_removes_orphans(self,
                                        ns_name,
                                        ns_parentless,
                                        cidr,
                                        address,
                                        hostname):
        self._namespace.create(ns_name)
        self._namespace.create(ns_parentless)
        self._address.create(cidr, address, hostname, ns_name)

        self._namespace.delete_all()

        result = self._namespace.find_by_name(ns_parentless)
        assert not result
        result = self._namespace.find_by_name(ns_name)
        assert result

    @data('test-namespace')
    def test_delete_by_name(self, name):
        self._namespace.create(name)

        result = self._namespace.delete_by_name(name)
        assert result

    @data('invalid')
    def test_delete_by_name_is_false_when_not_found(self, name):
        result = self._namespace.delete_by_name(name)
        assert not result

    @data('test-namespace')
    def test_find_by_name(self, name):
        self._namespace.create(name)

        result = self._namespace.find_by_name(name)
        self.assertEquals('test-namespace', result.name)

    @data('invalid')
    def test_find_by_name_is_false_when_not_found(self, name):
        result = self._namespace.find_by_name(name)
        assert not result
