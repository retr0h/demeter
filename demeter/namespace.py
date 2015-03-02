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

import demeter
from demeter import models


class Namespace(object):
    def create(self, name):
        if not self.find_by_name(name):
            ns = models.Namespace(name=name)
            with demeter.transactional_session() as session:
                session.add(ns)
                return ns

    def delete(self, ns):
        with demeter.transactional_session() as session:
            session.delete(ns)
            return True

    def delete_by_name(self, name):
        result = self.find_by_name(name)
        if result:
            with demeter.transactional_session() as session:
                session.delete(result)
                return True

    def find_by_name(self, name):
        with demeter.temp_session() as session:
            ns = models.Namespace
            return session.query(ns).filter_by(name=name).first()
