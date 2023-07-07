from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

with app.app_context():
	db.drop_all()
	db.create_all()
	# db.session.add_all(users)
	# db.session.add(user)
	# db.session.commit()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""
        with app.app_context():
          User.query.delete()

          user = User(first_name="TestUser", last_name="Muster")
          db.session.add(user)
          db.session.commit()

        # self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Muster Testuser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Muster Testuser</h1>', html)


    def test_add_user(self):
        """Test adding a new user."""
        with app.test_client() as client:
            data = {
                'first_name': 'a',
                'last_name': 'b',
                'image_url': 'None'
            }
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/2"\n        >B A</a\n      >', html)

# Run the app
if __name__ == '__main__':
	app.run()
  