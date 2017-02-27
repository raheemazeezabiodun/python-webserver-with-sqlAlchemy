from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

dbName = 'sqlite:///restaurant.db'
Base = declarative_base()
engine = create_engine(dbName)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Restaurant(Base):

    __tablename__ = 'restaurant'

    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)

    def save(self, name):
        if session.add(Restaurant(name=name)):
            session.commit()
            return True
        else:
            return False

    def fetch(self):
        allRestaurant = session.query(Restaurant).all()
        return allRestaurant

    def update(self, old, new):
        getRestaurant = session.query(Restaurant).filter_by(name=old).one()
        if getRestaurant != []:
            getRestaurant.name = new
            session.add(getRestaurant)
            session.commit()
            return True
        else:
            return False

    def delete(self, name):
        getRestaurantToDelete = session.query(Restaurant).filter_by(name=name).one()
        if getRestaurantToDelete != []:
            session.delete(getRestaurantToDelete)
            session.commit()
            return True
        else:
            return False


class MenuItem(Base):

    __tablename__ = 'menuItem'

    name = Column(String(50), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=False)
    price = Column(String(10), nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


if __name__ == "__main__":
    Base.metadata.create_all(engine)

