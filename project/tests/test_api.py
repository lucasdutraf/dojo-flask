import unittest

from project.tests.base import BaseTestCase

if __name__ == '__main__':
    unittest.main()


class TestApi(BaseTestCase):
    def test_api(self):
        self.assertTrue(True)