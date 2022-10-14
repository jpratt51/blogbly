"""Seed file to make sample data for pets db."""

from models import User, Post, db, connect_db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Post.query.delete()

# Add users
Alan = User(first_name='Alan', last_name='Alda', img_url='https://t3.ftcdn.net/jpg/02/94/62/14/360_F_294621430_9dwIpCeY1LqefWCcU23pP9i11BgzOS0N.jpg')
Joel = User(first_name='Joel', last_name='Burton', img_url='https://media.istockphoto.com/photos/portrait-smiling-african-american-businessman-in-blue-suit-sit-at-picture-id1341347262?b=1&k=20&m=1341347262&s=170667a&w=0&h=nWVSejAWgPgQi128JMemYKX0YX9xUgf18Nd3o4Ez6ic=')
Jane = User(first_name='Jane', last_name='Smith', img_url='https://www.iiba.org/contentassets/5fb09f91009640eba14f8d10711d5925/12-tips-for-balancing-header.png')

#Add posts
post1 = Post(title="Famouse Quote", content="'Fortune favors the bold.' -Virgil", user_id=1)
post2 = Post(title="Favorite Song This Week", content="'Ghost' by Justin Bieber", user_id=2)
post3 = Post(title="Try This New Recipe", content="Creamy Vegan Pasta", user_id=3)

# Add new objects to session, so they'll persist
db.session.add_all([Alan,Joel,Jane])

db.session.commit()

db.session.add_all([post1,post2,post3])

db.session.commit()