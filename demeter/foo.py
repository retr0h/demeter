import sqlalchemy
import sqlalchemy.orm

from demeter import client
from demeter.models import Address
from demeter.models import Tag

engine = client.get_engine()
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

t1 = Tag(name="dc1")
t2 = Tag(name="dc2")
t3 = Tag(name="dc3")
addr1 = Address(name="10.10.10.10", tag=t1)
addr2 = Address(name="20.20.20.20", tag=t2)
addr3 = Address(name="30.30.30.30", tag=t3)
addr4 = Address(name="50.50.50.50", tag=t1)
session.add(t1)
session.add(t2)
session.add(t3)
session.add(addr1)
session.add(addr2)
session.add(addr3)
session.add(addr4)
session.commit() 

print session.query(Tag).all()
print session.query(Address).all()

addresses = session.query(Address).all()
for address in addresses:
    print address.name + ":" + address.tag.name

print session.query(Address).filter(Address.name.startswith("10")).one().name
print session.query(Address).join(Address.tag).filter(
    Address.name.startswith('10'), Tag.name == 'dc1').all()[0].name

# Cleanup #
tags = session.query(Tag).all()
for tag in tags:
    session.delete(tag)
    session.commit() 
print session.query(Tag).all()
print session.query(Address).all()
