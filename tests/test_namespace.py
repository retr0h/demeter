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
import unittest2 as unittest

from demeter.namespace import Namespace


@ddt
class TestNamespace(unittest.TestCase):
    def uuid():
        return str(uuid.uuid4())

    def setUp(self):
        self._namespace = Namespace()

    @data(uuid())
    def test_create(self, name):
        ns = self._namespace.create(name)

        result = self._namespace.find_by_name(name)
        self.assertEquals(name, result.name)

        self._namespace.delete(ns)

    @data(uuid())
    def test_delete(self, name):
        ns = self._namespace.create(name)

        result = self._namespace.delete(ns)
        assert result
        result = self._namespace.find_by_name(name)
        assert not result

        self._namespace.delete(ns)

    @data(uuid())
    def test_delete_by_name(self, name):
        ns = self._namespace.create(name)

        result = self._namespace.delete_by_name(name)
        assert result

        self._namespace.delete(ns)

    @data('ns-not-found')
    def test_delete_by_name_is_false_when_not_found(self, name):
        result = self._namespace.delete_by_name(name)
        assert not result

    @data(uuid())
    def test_find_by_name(self, name):
        ns = self._namespace.create(name)

        result = self._namespace.find_by_name(name)
        self.assertEquals(name, result.name)

        self._namespace.delete(ns)

    @data('ns-not-found')
    def test_find_by_name_is_false_when_not_found(self, name):
        result = self._namespace.find_by_name(name)
        assert not result
