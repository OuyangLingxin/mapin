from unittest import TestCase
from server import app

class FlaskTests(TestCase):
  def setUp(self):
    self.client = app.test_client()
    app.config['TESTING'] = True

  def test1(self):
    result = self.client.get('/maps')
    self.assertEqual(result.status_code, 302)
    self.assertIn(b'Add New Employee', result.data)

  def test2(self):
    result = self.client.post('/',
                      data={'email':'11@test.test', 'password': '123456789'},
                      follow_redirects=True)
    self.assertIn(b'<a>Add New Employee</a>', result.data)

if __name__ == '__main__':
  import unittest
  unittest.main()