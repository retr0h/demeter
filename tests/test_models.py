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

import sqlalchemy
import sqlalchemy.exc
import unittest2 as unittest
from ddt import data
from ddt import ddt
from ddt import unpack

from demeter import client


@ddt
class TestModels(unittest.TestCase):
    def setUp(self):
        engine = client.get_engine()
        self._inspector = sqlalchemy.inspect(engine)

    @data(
        ('id', 'INTEGER', 'False'),
        ('namespace', 'VARCHAR(25)', 'False'),
        ('cidr', 'CIDR', 'False'),
        ('address', 'INET', 'False'),
        ('allocated', 'BOOLEAN', 'True'),
        ('hostname', 'VARCHAR(64)', 'True'),
    )
    @unpack
    def test_ipv4_address_schema(self, name, type, nullable):
        columns = self._inspector.get_columns('ipv4_address')
        for column in columns:
            if column.get('name') == name:
                self.assertEquals(type, str(column.get('type')))
                self.assertEquals(nullable, str(column.get('nullable')))

    def test_ipv4_address_has_hostname_to_namespace_uniq_costraint(self):
        constraints = self._inspector.get_unique_constraints('ipv4_address')
        constraint = constraints[0].get('column_names')
        expected = ['namespace', 'hostname']

        self.assertEquals(expected, constraint)
