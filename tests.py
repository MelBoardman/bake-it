# import the os
import os
# import the unittest package for python
import unittest
# import app from the app.py file
from app import app
class RoutingTests(unittest.TestCase):
    # function to set up testing connection
    def set_up(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        self.app = app.test_client()
        self.assertEqual(app.debug,False)
    # function to teardown connection after testing
    def tear_down(self):
        pass

    # function to test that the route for the homepage works
    def test_home(self):
        self.app = app.test_client()
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        # check for text specific to the home page (index.html)
        self.assertIn("with Pyrex", str(response.data))
    
    # function to test that the route for the log in page works
    def test_log_in(self):
        self.app = app.test_client()
        response = self.app.get("/log_in")
        self.assertEqual(response.status_code, 200)
        # check for text specific to the log in page (log_in.html)
        self.assertIn("Log In", str(response.data))
    
    # function to test that the route for the sign up page works
    def test_sign_up(self):
        self.app = app.test_client()
        response = self.app.get("/sign_up")
        self.assertEqual(response.status_code, 200)
        # check for text specific to the log in page (sign_up.html)
        self.assertIn("Sign Up", str(response.data))
    
    # function to test that the route for the sign up page works
    def test_get_recipes(self):
        self.app = app.test_client()
        response = self.app.get("/get_recipes")
        self.assertEqual(response.status_code, 200)
        # check for text specific to the log in page (sign_up.html)
        self.assertIn("category", str(response.data))

if __name__ == "__main__":
    unittest.main()

