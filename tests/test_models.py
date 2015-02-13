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

import sqlalchemy.exc
import sqlalchemy.orm as orm
import unittest2 as unittest
from ddt import ddt, data

from demeter import client
from demeter.models import Ipv4Address


@ddt
class TestModels(unittest.TestCase):
    def _cleanup(self):
        addresses = self._session.query(Ipv4Address).all()
        for address in addresses:
            self._session.delete(address)
        self._session.commit() 

    def setUp(self):
        engine = client.get_engine()
        Session = orm.sessionmaker(bind=engine)
        self._session = Session()
        self._cleanup()

    @data(
        {'pool_cidr': '10/8', 'address': '10.0.0.1', 'allocated': True},
        {'pool_name': 'test_pool', 'address': '10.0.0.1', 'allocated': True},
        {'pool_name': 'test_pool', 'pool_cidr': '10/8', 'allocated': True},
        {'pool_name': 'test_pool', 'pool_cidr': '10/8', 'address': '10.0.0.1'}
    )
    def test_ipv4_address_raises_when_required_fields_not_present(self, value):
        ia = Ipv4Address(**value)
        self._session.add(ia)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self._session.commit()

    @data(
        {'pool_name': 'test_pool',
         'pool_cidr': 'invalid',
         'address': '10.1.1.1',
         'allocated': True},
        {'pool_name': 'test_pool',
         'pool_cidr': '10/8',
         'address': 'invalid',
         'allocated': True},
        {'pool_name': 'test_pool',
         'pool_cidr': '10/8',
         'address': '10.1.1.1',
         'allocated': 'invalid'},
    )
    def test_ipv4_address_raises_on_invalid_table_type(self, value):
        ia = Ipv4Address(**value)
        self._session.add(ia)
        with self.assertRaises(sqlalchemy.exc.DataError):
            self._session.commit()

    def test_ipv4_address_has_proper_table_type(self):
        ia = Ipv4Address(pool_name='test_pool',
                         pool_cidr='10/8',
                         address='10.1.1.1',
                         allocated=True)
        self._session.add(ia)
        self._session.commit()

        response = self._session.query(Ipv4Address).first()
        self.assertEquals('test_pool', response.pool_name)
        self.assertEquals('10.0.0.0/8', response.pool_cidr)
        self.assertEquals('10.1.1.1', response.address)
        assert response.allocated

        self._session.delete(ia)
