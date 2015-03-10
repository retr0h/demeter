api
===

Namespaces
==========

Create
------

/namespace/:name POST

.. code-block:: javascript

    {
      "cidr": "198.51.100.0/24"
    }

Delete
------

/namespace/:name

List
----

/namespaces

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
