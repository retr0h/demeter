import sqlalchemy
import sqlalchemy.orm

from demeter import client
from demeter.models import Namespace

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = client.get_engine()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

# session.query(Ipv4Address).delete()
# session.commit()

# addresses = session.query(Ipv4Address).all()
# for address in addresses:
#     session.delete(address)
# session.commit()

# ns = Namespace(name='shit-1')
# addr = Ipv4Address(cidr='10.10.10.0/24',
#                    address='10.10.10.1',
#                    hostname='fuck off',
#                    namespace=ns)
# session.add(ns)
# session.add(addr)
# session.commit()

f = session.query(Namespace).all()
for i in f:
    print i.name
    print i.address.cidr

# f = session.query(Namespace).join(Namespace.address).filter(
#     Namespace.name == 'shit-1', Ipv4Address.cidr == '10.10.10.0/23').first()

# print f.name
# print f.address

# for i in f:
#     print i.name
#     print i.address.cidr


# print session.query(Address).filter(Address.name.startswith("10")).one().name
