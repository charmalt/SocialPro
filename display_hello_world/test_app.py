from unittest import TestCase

from display_hello_world import hello_world
from display_hello_world.config import host, port


class TestHelloWorld(TestCase):

    def setUp(self):
        self.app = hello_world.app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_prints_hello_world(self):
        url = 'http://{}:{}/'.format(host, port)
        response = self.app.get(url)
        self.assertEqual(b'Hello World', response.data)
