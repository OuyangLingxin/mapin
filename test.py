from unittest import TestCase
from server import app
from model import connect_to_db

class FlaskTests(TestCase):
  def setUp(self):
    self.client = app.test_client()
    app.config['TESTING'] = True

  def test1(self):
    result = self.client.get('/', follow_redirects=True)
    self.assertEqual(result.status_code, 200)

  def test2(self):
    result = self.client.post('/',
                      data={'email':'11@test.test', 'password': '123456789'},
                      follow_redirects=True)
    self.assertIn(b'<div\n  id="map"\n  class="m-auto object-fit-scale border rounded mb-4"\n  heigh="90%"\n></div>', result.data)

if __name__ == '__main__':
  import unittest
  connect_to_db(app)
  unittest.main()