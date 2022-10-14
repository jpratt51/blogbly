from unittest import TestCase

from app import app
from models import db, connect_db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

connect_db(app)
db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        Post.query.delete()
        User.query.delete()

        user = User(first_name='Alan', last_name='Alda', img_url='https://t3.ftcdn.net/jpg/02/94/62/14/360_F_294621430_9dwIpCeY1LqefWCcU23pP9i11BgzOS0N.jpg')

        db.session.add(user)
        db.session.commit()

        self.users_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users_page(self):
        """Test redirects to users page and correctly displays html"""
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Users', html)

    def test_user_details_page(self):
        """Test correctly routing to user details page and displays user name"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.users_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Alan Alda', html)

    def test_edit_user_form(self):
        """Test correctly routing to user edit page and displays correct html"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.users_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Edit User</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:

            d = {"first_name": "Joel", "last_name": "Burton", "img_url": "https://media.istockphoto.com/photos/portrait-smiling-african-american-businessman-in-blue-suit-sit-at-picture-id1341347262?b=1&k=20&m=1341347262&s=170667a&w=0&h=nWVSejAWgPgQi128JMemYKX0YX9xUgf18Nd3o4Ez6ic="}

            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Joel Burton", html)

    def test_add_post_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.users_id}/new-post")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Add Post for Alan Alda', html)

    def test_post_details(self):
        with app.test_client() as client:
            d = {"title": "Famouse Quote", "content": "'Fortune favors the bold.' -Virgil"}

            resp = client.post(f"/users/{self.users_id}/new-post", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Famouse Quote', html)