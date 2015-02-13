import sqlalchemy
import sqlalchemy.orm

from demeter import client
from demeter.models import Ipv4Address

engine = client.get_engine()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

ia = Ipv4Address(pool_name='test_pool',
                 pool_cidr='10.1.1.0/24',
                 addr='10.1.1.5')
session.add(ia)
session.commit()

# print session.query(Address).filter(Address.name.startswith("10")).one().name
# print session.query(Address).join(Address.tag).filter(
#     Address.name.startswith('10'), Tag.name == 'dc1').all()[0].name
