"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, PostTag, db
from app import app

# If tables aren't empty, empty them
# PostTag.query.delete()
# User.query.delete()
# Tag.query.delete()
# Post.query.delete()

# Create all tables
db.drop_all()
db.create_all()

# Add users
Alan = User(first_name='Alan', last_name='Alda', img_url='https://t3.ftcdn.net/jpg/02/94/62/14/360_F_294621430_9dwIpCeY1LqefWCcU23pP9i11BgzOS0N.jpg')
Joel = User(first_name='Joel', last_name='Burton', img_url='https://media.istockphoto.com/photos/portrait-smiling-african-american-businessman-in-blue-suit-sit-at-picture-id1341347262?b=1&k=20&m=1341347262&s=170667a&w=0&h=nWVSejAWgPgQi128JMemYKX0YX9xUgf18Nd3o4Ez6ic=')
Jane = User(first_name='Jane', last_name='Smith', img_url='https://www.iiba.org/contentassets/5fb09f91009640eba14f8d10711d5925/12-tips-for-balancing-header.png')

#Add posts
post1 = Post(title="Famouse Quote", content="'Fortune favors the bold.' -Virgil", user_id=1)
post2 = Post(title="Favorite Song This Week", content="'Ghost' by Justin Bieber", user_id=2)
post3 = Post(title="Try This New Recipe", content="Creamy Vegan Pasta", user_id=3)
post4 = Post(title="Easy Bean Casserole", content="Follow this link! www.brokenlink.com", user_id=1)
post5 = Post(title="Inspirational Quote", content="'When you have a dream, you've got to grab it and never let go' -Carol Burnett", user_id=2)
post6 = Post(title="New Song Release", content="'The Drummer' by Red Hot Chili Peppers", user_id=3)

#Add Tags
tag1 = Tag(name="#quote")
tag2 = Tag(name="#song")
tag3 = Tag(name="#recipe")
tag4 = Tag(name="#new")

#add tags to posts
post1.tags.append(tag1)

post2.tags.append(tag2)

post3.tags.append(tag3)

post3.tags.append(tag4)

post4.tags.append(tag3)

post5.tags.append(tag1)

post6.tags.append(tag2)

post6.tags.append(tag4)

# Add new objects to session, so they'll persist
db.session.add_all([Alan,Joel,Jane])

db.session.commit()

db.session.add_all([post1,post2,post3,post4,post5,post6])

db.session.commit()

db.session.add_all([tag1, tag2, tag3, tag4])

