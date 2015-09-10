import os
import unittest
import test.utils.mongod as mongod


class TestMedium(unittest.TestCase):

    DB_SETTINGS = {'HOST': ['localhost'],      # IP the database server
                   'PORT': 27917,              # PORT that mongodb is listening
                   'DB_NAME': 'pyuss',    # Name of the database
                   'REPLSET': ''}

    @classmethod
    def setUpClass(cls):
        db_dir = os.path.join(os.path.dirname(__file__), "..") + "/db"
        mongo = mongod.Mongod(port=cls.DB_SETTINGS['PORT'], db_path=db_dir)
        mongo.start()

    @classmethod
    def tearDownClass(cls):
        db_dir = os.path.join(os.path.dirname(__file__), "..") + "/db"
        mongo = mongod.Mongod(port=cls.DB_SETTINGS['PORT'], db_path=db_dir)
        mongo.stop()

    def tearDown(self):
        pass

    def test_test1(self):

        self.assertEquals(1, 1)

if __name__ == "__main__":
    unittest.main()
