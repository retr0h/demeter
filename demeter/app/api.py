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

from flask import Flask
from flask import json
from flask import request

from demeter.namespace import Namespace
from demeter.address import Address


app = Flask(__name__)


@app.route('/v1.0/status', methods=['GET'])
def get_index():
    return json.dumps({'success': True})


@app.route('/v1.0/namespace/<name>', methods=['DELETE'])
def delete_namespace(name):
    namespace = Namespace()
    ns = namespace.find_by_name(name)
    Namespace().delete(ns)

    return json.dumps({'success': True})


@app.route('/v1.0/namespace', methods=['POST'])
def create_namespace():
    data = request.get_json()
    ns = Namespace().create(data.get('name'),
                            data.get('cidr'))
    if ns:
        return json.dumps({'namespace': {'name': ns.name,
                                         'cidr': ns.cidr}})
    else:
        return json.dumps({}), 409


@app.route('/v1.0/address', methods=['POST'])
def create_address():
    """ Testing general workflow """
    data = request.get_json()

    namespace = data.get('namespace')
    cidr = data.get('cidr')
    hostname = data.get('hostname')

    Namespace().create(namespace, cidr)
    a = Address().next(namespace, hostname)
    return json.dumps({'address': a.address})


def run():
    app.run(debug=True)
