demeter
=======

TODO

Usage
=====

.. code-block:: bash

	$ demeter -h

Manually executing the writer:

.. code-block:: bash

	$ PYTHONPATH=$PYTHONPATH:. python demeter/shell.py

Testing
=======

Requirements:

* Ansible >= 1.6
* Vagrant >= 1.6
* Tox

Execute unit tests:

.. code-block:: bash

	$ make test

Execute a single test:

.. code-block:: bash

    $ source .tox/py27/bin/activate
    $ python -m testtools.run tests/app/test_api.py

Contents:

.. toctree::
   :maxdepth: 2

   address
   api
   client
   config
   models
   namespace

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
