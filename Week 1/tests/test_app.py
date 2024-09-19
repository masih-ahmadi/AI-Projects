import unittest
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_check_text(self):
        response = self.app.post('/check-text', json={'text': 'You are awesome!'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('is_toxic', data)
        self.assertFalse(data['is_toxic'])

if __name__ == '__main__':
    unittest.main()
