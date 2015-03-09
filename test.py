import demeter
from demeter import models
from demeter import namespace
from demeter import address

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

name = 'foo-namespace'
namespace.Namespace().create(name, '198.51.100.0/24')
addr = address.Address()
ns = namespace.Namespace().find_by_name(name)

addr1 = {'address': '198.51.100.1',
         'address_int': 3325256705,
         'hostname': 'addr1-hostname',
         'namespace': ns}
addr2 = {'address': '198.51.100.2',
         'address_int': 3325256706,
         'hostname': 'addr2-hostname',
         'namespace': ns}
addr3 = {'address': '198.51.100.3',
         'address_int': 3325256707,
         'hostname': 'addr3-hostname',
         'namespace': ns}
addr4 = {'address': '198.51.100.4',
         'address_int': 3325256708,
         'hostname': 'addr4-hostname',
         'namespace': ns}

a1 = addr.create(**addr1)
a2 = addr.create(**addr2)
a3 = addr.create(**addr3)
a4 = addr.create(**addr4)

addr.delete(a3)

with demeter.temp_session() as session:
    ns = models.Namespace
    addr = models.Ipv4Address
    q = session.query(ns).outerjoin(ns.addresses).filter(
        ns.name == name).first()
    print q.cidr

    for a in q.addresses:
        print a.address
