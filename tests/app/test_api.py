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
from flask import json
import unittest2 as unittest

from demeter.app import api as app
from tests import helper


@ddt
class TestApi(unittest.TestCase):
    def setUp(self):
        self._app = app.app.test_client()

    def post(self, url, data):
        return self._app.post(url,
                              content_type='application/json',
                              data=json.dumps(data))

    def test_app_index(self):
        response = self._app.get('/v1.0/status')
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(True, data['success'])

    def test_app_all_namespaces(self):
        response = self._app.get('/v1.0/namespaces')
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        assert 0 <= len(data['namespace'])  # shitty test really

    @unpack
    @data(helper.namespace_data())
    def test_app_create_namespace(self, ns_name, cidr):
        url = '/v1.0/namespace/{0}'.format(ns_name)
        response = self.post(url, {"cidr": cidr})

        data = json.loads(response.data)
        self.assertEquals(200, response.status_code)
        self.assertEquals(ns_name, data['namespace']['name'])
        self.assertEquals(cidr, data['namespace']['cidr'])

        self._app.delete(url)

    @unpack
    @data(helper.namespace_data())
    def test_app_create_namespace_returns_409_when_exists(self, ns_name, cidr):
        url = '/v1.0/namespace/{0}'.format(ns_name)
        self.post(url, {"cidr": cidr})
        response = self.post(url, {"cidr": cidr})

        self.assertEquals(409, response.status_code)

        self._app.delete(url)
