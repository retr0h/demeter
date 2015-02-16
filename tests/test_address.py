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

import sqlalchemy.orm as orm

import unittest2 as unittest
from ddt import data
from ddt import ddt
from ddt import unpack

from demeter import Address
from demeter import client
from demeter.models import Ipv4Address


@ddt
class TestAddress(unittest.TestCase):
    def _cleanup(self):
        addresses = self._session.query(Ipv4Address).all()
        for address in addresses:
            self._session.delete(address)
        self._session.commit()

    def setUp(self):
        self._address = Address.Address()
        engine = client.get_engine()
        Session = orm.sessionmaker(bind=engine)
        self._session = Session()
        self._cleanup()

    def test_valid_network(self):
        result = self._address._valid_network('192.0.2.0/24')

        self.assertEquals(256, len(result))

    @data(
        (24, 256),
        (25, 128),
        (26, 64),
        (27, 32),
        (28, 16),
        (29, 8),
        (30, 4),
        (31, 2),
        (32, 1),
    )
    @unpack
    def test_allocate(self, value, expected):
        cidr = '192.168.2.0/{0}'.format(value)
        namespace = 'test_namespace_{0}'.format(value)
        self._address.allocate(namespace, cidr)

        results = self._session.query(Ipv4Address).filter(
            Ipv4Address.namespace == namespace).all()

        self.assertEquals(expected, len(results))

    def test_allocate_raises_with_invalid_network(self):
        cidr = '192.0.2.0/36'

        with self.assertRaises(Address.InvalidNetworkException):
            self._address.allocate('test_namespace', cidr)

    def test_allocate_raises_with_address_(self):
        cidr = '192.0.2.0/22'

        with self.assertRaises(Address.NetworkNotAllowedException):
            self._address.allocate('test_namespace', cidr)
