import demeter
from demeter import models
from demeter import namespace
from demeter import address

name = 'foo-namespace'
namespace.Namespace().create(name)
addr = address.Address()
ns = namespace.Namespace().find_by_name(name)

addr1 = {'cidr': '198.51.100.0/24',
         'address': '198.51.100.1',
         'address_int': 3325256705,
         'hostname': 'addr1-hostname',
         'namespace': ns}
addr2 = {'cidr': '198.51.100.0/24',
         'address': '198.51.100.2',
         'address_int': 3325256706,
         'hostname': 'addr2-hostname',
         'namespace': ns}
addr3 = {'cidr': '198.51.100.0/24',
         'address': '198.51.100.3',
         'address_int': 3325256707,
         'hostname': 'addr3-hostname',
         'namespace': ns}
addr4 = {'cidr': '198.51.100.0/24',
         'address': '198.51.100.4',
         'address_int': 3325256708,
         'hostname': 'addr4-hostname',
         'namespace': ns}

a1 = addr.create(**addr1)
a2 = addr.create(**addr2)
a3 = addr.create(**addr3)
a4 = addr.create(**addr4)

addr.delete(a3)

# how to determine the gap `delete(a3)` caused.
# we want to fill before we find largest int and +1.
with demeter.temp_session() as session:
    ns = models.Namespace
    addr = models.Ipv4Address
    f = session.query(ns).join(ns.addresses).filter(
        ns.name == name).order_by(addr.address_int)
    for k in f:
        print k.name
        for a in k.addresses:
            print a.address + ' ' + ' ' + str(a.address_int)
