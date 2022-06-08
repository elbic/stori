from django.test import TestCase


class IndexViewTest(TestCase):
    def setUp(self):
        pass

    def test_authenticated_user(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
