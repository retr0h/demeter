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

import json


class Config(object):
    """
    A class which handles the configuration of demeter.
    """

    def __init__(self, **kwargs):
        config_file = kwargs.get('config_file', '/etc/demeter.json')
        self._config = self._get_config(config_file)

    @property
    def db_url(self):
        c = self._config
        db_scheme = c.get('db_scheme', 'postgresql')
        db_user = c.get('db_user', 'demeter_user')
        db_pass = c.get('db_pass', 'pass')
        db_host = c.get('db_host', '192.168.100.11')
        db_port = c.get('db_port', 5432)
        db_name = c.get('db_name', 'demeter')

        return "{0}://{1}:{2}@{3}:{4}/{5}".format(db_scheme,
                                                  db_user,
                                                  db_pass,
                                                  db_host,
                                                  db_port,
                                                  db_name)

    def _get_config(self, config_file):
        try:
            return json.load(open(config_file))
        except IOError:
            return dict()
