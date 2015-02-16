import sqlalchemy
import sqlalchemy.orm

from demeter import client
# from demeter.models import Ipv4Address

engine = client.get_engine()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

# c = inspector.get_columns('ipv4_address')
# print any(d['name'] == 'id' for d in c)

# print("Column: %s" % column['type'])

# metadata = sqlalchemy.MetaData(bind=engine)
# messages = sqlalchemy.Table('ipv4_address',
#                             metadata,
#                             autoload=True,
#                             autoload_with=engine)

# ia = Ipv4Address(pool_name='test_pool_1',
#                  pool_cidr='10.1.1.0/24',
#                  address='10.1.1.5',
#                  hostname='host')
# session.add(ia)

# ia = Ipv4Address(pool_name='test_pool_2',
#                  pool_cidr='10.1.1.0/24',
#                  address='10.1.1.5',
#                  hostname='host')
# session.add(ia)

# session.commit()

# print session.query(Address).filter(Address.name.startswith("10")).one().name
# print session.query(Address).join(Address.tag).filter(
#     Address.name.startswith('10'), Tag.name == 'dc1').all()[0].name
