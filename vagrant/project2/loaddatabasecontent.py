from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Category, Item, Base, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()
# Add my info
User1 = User(name="Jamie Gambrell", email="stingray72@gmail.com")
session.add(User1)
session.commit()


#
category1 = Category(user_id=1, name="Football")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Shoes", description="Shoes with cleats",
             category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Football", description="Regulation \
             football", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Jersey", description="NFL style jersey for \
             Atlanta Falcons size xlg", category=category1)

session.add(item3)
session.commit()


#
category2 = Category(user_id=1, name="Soccer")

session.add(category2)
session.commit()


item1 = Item(user_id=1, name="Soccer ball", description="Regulation \
             black and white ball", category=category2)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Shoes", description="Regulation shoes with \
             removable cleats size 12", category=category2)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Whistle", description="Standard sports \
             whistle", category=category2)

session.add(item3)
session.commit()


# Menu for Panda Garden
category1 = Category(user_id=1, name="Fishing")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Tackle box", description="Plano model 12, 3 \
             tier box", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Fly rod", description="Bamboo hand made rod \
             without a reel", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Fly reel", description="BKG model 18 stainless \
             steal reel", category=category1)

session.add(item3)
session.commit()

item4 = Item(user_id=1, name="Flys", description="Assortment of 24 flies",
             category=category1)

session.add(item4)
session.commit()

category1 = Category(user_id=1, name="Woodworking")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Safety glasses", description="3M clear safety \
             glasses with clear lens", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Bandsaw", description="Jet 18 inch bandsaw \
             model 818 with blade", category=category1)

session.add(item2)
session.commit()

item3 = Item(user_id=1, name="Tablesaw", description="Delta cabinet saw with \
             10 inch blade", category=category1)

session.add(item3)
session.commit()

category1 = Category(user_id=1, name="Knitting")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Knitting needles", description="Set of needles \
in small, medium and large", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Yarn", description="Assortment of 5 rolls of \
various colored yarn", category=category1)

session.add(item2)
session.commit()


# Menu for Auntie Ann's
category1 = Category(user_id=1, name="Sewing")

session.add(category1)
session.commit()

item9 = Item(user_id=1, name="Sewing machine", description="Singer model 4",
             category=category1)

session.add(item9)
session.commit()

item1 = Item(user_id=1, name="Needles", description="Assortment of 24 needles \
in bulk package", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Pattern", description="Assortment of 30 shirt \
patterns", category=category1)

session.add(item2)
session.commit()


# Menu for Cocina Y Amor
category1 = Category(user_id=1, name="Hunting")

session.add(category1)
session.commit()


item1 = Item(user_id=1, name="Safety vest", description="Orange safety vest, \
one size fits most", category=category1)

session.add(item1)
session.commit()

item2 = Item(user_id=1, name="Game bag", description="Camo colored two gallon \
canvas bag with draw string", category=category1)

session.add(item2)
session.commit()

print("added items!")
