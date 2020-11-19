from db import Customers, engine
from sqlalchemy.orm import sessionmaker

connection = engine.connect()
Session = sessionmaker(bind = engine)
session = Session()
c1, c2, c3 = Customers(name="Вова", address="мкр. Северный д. 34", email="tes13@gmail.com"), \
	Customers(name="Тима", address="мкр. Олимпийский д. 34", email="tes13333333333@gmail.com"), \
	Customers(name="Тоха", address="мкр. Космос д. 34", email="tes13111@gmail.com")

session.add_all([c1, c2, c3])
print(session.query(Customers).all())