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
        self._ns_name, self._ns_cidr, self._family = helper.namespace_data()

    def _create_namespace(self, ns_name, cidr, family):
        url = self.namespace_url(ns_name)
        return self._post(url, {'cidr': cidr, 'family': family})

    def _delete_namespace(self, url):
        url = self.namespace_url(self._ns_name)
        return self._app.delete(url)

    def _post(self, url, data):
        return self._app.post(url,
                              content_type='application/json',
                              data=json.dumps(data))

    def setup_teardown_namespace(func):
        def wrapper(self, *args, **kwargs):
            self._create_namespace(self._ns_name, self._ns_cidr, self._family)

            func(self, *args, **kwargs)

            self._delete_namespace(self._ns_name)
        return wrapper

    def namespace_url(self, ns_name):
        return '/v1.0/namespace/{0}'.format(ns_name)

    def test_app_index(self):
        response = self._app.get('/v1.0/status')
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(True, data['success'])

    @setup_teardown_namespace
    def test_app_all_namespaces(self):
        response = self._app.get('/v1.0/namespaces')
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        assert self._ns_name in data['namespace']

    @unpack
    @data(helper.namespace_data())
    def test_app_create_namespace(self, ns_name, cidr, family):
        response = self._create_namespace(ns_name, cidr, family)
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(ns_name, data['namespace']['name'])
        self.assertEquals(cidr, data['namespace']['cidr'])
        self.assertEquals('inet', data['namespace']['family'])

        self._delete_namespace(ns_name)

    @unpack
    @data(helper.namespace_data())
    def test_app_create_namespace_returns_409_when_exists(self,
                                                          ns_name,
                                                          cidr,
                                                          family):
        self._create_namespace(ns_name, cidr, family)
        response = self._create_namespace(ns_name, cidr, family)

        self.assertEquals(409, response.status_code)

        self._delete_namespace(ns_name)

    @setup_teardown_namespace
    def test_app_show_namespace(self):
        url = self.namespace_url(self._ns_name)
        # TODO(retr0h): populate address
        response = self._app.get(url)
        data = json.loads(response.data)

        self.assertEquals(200, response.status_code)
        self.assertEquals(self._ns_name, data['namespace']['name'])
        self.assertEquals('198.51.100.0/24', data['namespace']['cidr'])
        self.assertEquals('inet', data['namespace']['family'])
