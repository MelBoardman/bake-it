# import the Os
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
    def test_home(self):
        self.app = app.test_client()
        response = self.app.get("/")
        print(response.data)
        self.assertEqual(response.status_code, 200)
        # self.assertIn("share", response)
        
if __name__ == "__main__":
    unittest.main()

# from app import app
# from unittest import TestCase

# class TestRoutes(unittest.TestCase):
#     self.app = app.test_client()
#     def test_home_page(self):
#         response = self.app.get("/")
#         print(response.data)
#         self.assertEqual(response.status_code, 200)
#         self.assertIn("share it", response )
 
# if __name__ == "__main__":
#     unittest.main()