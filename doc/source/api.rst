api
===

Namespaces
==========

All
---

/namespaces GET

Response data

.. code-block:: javascript

    {
      "namespace": [
        "namespace-1",
        "namespace-2"
      ]
    }

Create
------

/namespace/:name POST

Request data

.. code-block:: javascript

    {
      "cidr": "198.51.100.0/24"
    }

Response data

.. code-block:: javascript

    {
      "namespace": {
        "name": "namespace-name",
        "cidr": "198.51.100.0/24"
      }
    }

Delete
------

/namespace/:name DELETE

Response data

.. code-block:: javascript

    {
      "namespace": {
        "success": True|False
      }
    }

Show
----

/namespace/:name GET

Address
=======

Reserve
-------

/address POST

.. code-block:: javascript

    {
      "namespace": "test-namespace",
      "hostname": "test-hostname"
    }


.. code-block:: bash

    $ curl -X POST -H "Content-Type: application/json" -d '{"namespace":"curl-test-5","cidr":"192.100.200.0/29", "hostname": "hostname"}'  http://127.0.0.1:5000/v1.0/address
