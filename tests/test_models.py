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

from demeter import client
from demeter.models import Address
from demeter.models import Tag


class TestModels(unittest.TestCase):
    def _cleanup(self):
        tags = self._session.query(Tag).all()
        for tag in tags:
            self._session.delete(tag)
            self._session.commit() 

    def setUp(self):
        engine = client.get_engine()
        Session = orm.sessionmaker(bind=engine)
        self._session = Session()
        self._cleanup()

    def test_tag_requires_a_name(self):
        tag = Tag(name='tag')
        self._session.add(tag)
        self._session.commit()

        response = self._session.query(Tag).first()
        self.assertEquals('tag', response.name)

        self._session.delete(tag)

    def test_tag_name_has_a_unique_constraint(self):
        tag1 = Tag(name='tag-1')
        tag2 = Tag(name='tag-1')
        self._session.add(tag1)
        self._session.add(tag2)
        with self.assertRaises(sqlalchemy.exc.IntegrityError):
            self._session.commit()
