import unittest
import transaction

from pyramid import testing

from .models import DBSession

class TestGenericQuestion(unittest.TestCase):
    """ A class for testing the functions in the Question class in
        games/base.py that do their own work, as opposed to the ones that get
        subclassed/overriden.
    """

    def setUp(self):
        self.config = testing.setUp()
        from .games import base
        self.my_question = base.Question()

    def tearDown(self):
        testing.tearDown()

    def test_validate_wrong_percent(self):
        self.assertIsNone(self.my_question._validate_wrong_percent(50.0, 50.0))
        self.assertIsNone(self.my_question._validate_wrong_percent(49.1, 50.0))
        self.assertIsNone(self.my_question._validate_wrong_percent(50.9, 50.0))
        self.assertIsNone(self.my_question._validate_wrong_percent(100.01, 50.0))
        self.assertEqual(self.my_question._validate_wrong_percent(45.0, 50.0), 45.0)

    def test_validate_wrong_int(self):
        self.assertIsNone(self.my_question._validate_wrong_int(4, 4))
        self.assertIsNone(self.my_question._validate_wrong_int(12, 4, answer_ceiling=5))
