import os
import unittest
import test.utils.mongod as mongod


class TestLarge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db_dir = os.path.join(os.path.dirname(__file__), "..") + "/db"
        mongo = mongod.Mongod(port=27917, db_path=db_dir)
        mongo.start()

    @classmethod
    def tearDownClass(cls):
        db_dir = os.path.join(os.path.dirname(__file__), "..") + "/db"
        mongo = mongod.Mongod(port=27917, db_path=db_dir)
        mongo.stop()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test1(self):

        self.assertEquals(1, 1)

if __name__ == "__main__":
    unittest.main()
