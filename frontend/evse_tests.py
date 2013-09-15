import os
import evse
import unittest

class EvseTestCase(unittest.TestCase):
	def setUp(self):
		db_location = "localhost"
		db_username = "tesla"
		db_password = "tesla"
		db_database = "tesla_test"	
		evse.init_db(db_location, db_username, db_password, db_database)
		self.app = evse.app.test_client()
		self.app.secret_key = os.urandom(30)

	def tearDown(self):
		evse.close_db()

	def test_index_available(self):
		rv = self.app.get("/")
		assert "Get access to all your electric" in rv.data

	def test_login_available(self):
		rv = self.app.get("/login")
		#print rv.data
		assert "Please sign in" in rv.data

	def login(self, username, password):
		return self.app.post("/login", data=dict(username=username, password=password), follow_redirects=True)

	def logout(self):
		return self.app.get("/logout", follow_redirects=True)

	def test_login_logout(self):
		rv = self.login("test", "secret")
		assert "You were logged in" in rv.data
		rv = self.logout()
		assert "Get access to all your electric" in rv.data
		rv = self.login("test", "test")
		assert "Invalid username or password" in rv.data
		rv = self.login("bliepunexistinguser234", "lkjkl")
		assert "Invalid username or password" in rv.data

	def test_change_password(self):
		rv = self.app.get("/change-password")
		assert "logout" in rv.data
		rv = self.login("test", "secret")
		rv = self.app.post("/change-password", data=dict(oldpassword="test", newpassword1="a", newpassword2="a"))
		assert "Invalid passwo" in rv.data
		rv = self.app.post("/change-password", data=dict(oldpassword="secret", newpassword1="ljk", newpassword2="lkjlkj"))
		assert "Passwords do not match" in rv.data
		rv = self.app.post("/change-password", data=dict(oldpassword="secret", newpassword1="secret", newpassword2="secret"))
		print rv.data
		assert "Password successfully chan" in rv.data


if __name__ == "__main__":
	unittest.main()
