from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Table, desc  # This will talk directly to the database using the raw SQL commands
from sqlalchemy.orm import sessionmaker  # This is the equivalent to a psycopg2 cursor - allows you to queue up and execute database transactions
from sqlalchemy.ext.declarative import declarative_base  # This acts like a repository for the models, and will issue the create table statements to build up the database's table structure.
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from sqlalchemy import Column, Integer, String, Date, ForeignKey  # adding relationships
from sqlalchemy.orm import relationship                           # adding relationships

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base): 
    '''this is the tbay item model.'''    
    __tablename__ = "items"                                 # used to name the items table in the database
    id = Column(Integer, primary_key=True)                  # column1 - integer primary key
    name = Column(String, nullable=False)                   # column2 - name of item - string (can't be null)
    description = Column(String)                            # column3 - description of item - string 
    start_time = Column(DateTime, default=datetime.utcnow)  # column4 - auction start time - DateTime Object

    bids = relationship("Bid", backref="bid")
    
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
   
class User(Base): 
    '''this is the tbay user model.'''    
    __tablename__ = "users"                                  # used to name the user table in the database
    id = Column(Integer, primary_key=True)                  # column1 - integer primary key
    username = Column(String, nullable=False)               # column2 - username of user - string (can't be null)
    password = Column(String, nullable=False)               # column3 - password of user - string (can't be null) 

    item = relationship("Item", backref="owner")
    bid = relationship("Bid", backref="bidder")
    
class Bid(Base): 
    '''this is the tbay bid model.'''    
    __tablename__ = "bids"                                      # used to name the bid table in the database
    id = Column(Integer, primary_key=True)                      # column1 - integer primary key
    price = Column(Float, nullable=False)                       # column2 - floating point price - string (can't be null)
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)   
    
    
Base.metadata.create_all(engine)  # This creates a new table for each subclass of Base, ignoring any tables which already exist in the database

#add 3 users to database
lukebarry = User(username="luke", password="barry35")
benbarry = User(username="ben", password="barry32")
timbarry = User(username="tim", password="barry37")

session.add_all([timbarry, lukebarry, benbarry])
session.commit()

session.query(User).all()

#have user sell a baseball
baseball = Item(name="baseball", description="Roberto Clemente's 3000th hit", owner=lukebarry)
session.add(baseball)
session.commit()
print("{} is selling {} at {}".format(baseball.owner.username, baseball.name, baseball.start_time))

#have other users bid on baseball
startingbid = Bid(price = 100000, item_id = baseball.id, bidder = lukebarry)
benbid = Bid(price = 101000, item_id = baseball.id, bidder = benbarry)
timbid = Bid(price = 102000, item_id = baseball.id, bidder = timbarry)

bid_list = [timbid, benbid]

session.add(startingbid)
session.commit()

for bid in bid_list:
    print("{} bid on the {} for ${}".format(bid.bidder.username, baseball.name, bid.price))










