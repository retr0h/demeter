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
import sqlalchemy
import unittest2 as unittest

from demeter import client


@ddt
class TestModels(unittest.TestCase):
    def setUp(self):
        engine = client.get_engine()
        self._inspector = sqlalchemy.inspect(engine)

    @data(
        ('namespaces', 'id', 'INTEGER', 'False'),
        ('namespaces', 'name', 'VARCHAR(36)', 'False'),
        ('namespaces', 'cidr', 'CIDR', 'False'),
        ('ipv4_addresses', 'id', 'INTEGER', 'False'),
        ('ipv4_addresses', 'address', 'INET', 'False'),
        ('ipv4_addresses', 'address_int', 'NUMERIC(10, 0)', 'False'),
        ('ipv4_addresses', 'hostname', 'VARCHAR(64)', 'True'),
    )
    @unpack
    def test_model_schema(self, table, col_name, col_type, nullable):
        columns = self._inspector.get_columns(table)
        for column in columns:
            if column.get('name') == col_name:
                self.assertEquals(col_type, str(column.get('type')))
                self.assertEquals(nullable, str(column.get('nullable')))

    def test_namespace_table_has_name_to_cidr_unique_costraint(self):
        constraints = self._inspector.get_unique_constraints('namespaces')
        constraint = constraints[0].get('column_names')
        expected = ['name']

        self.assertEquals(expected, constraint)
