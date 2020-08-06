from django.test import SimpleTestCase, TestCase


class SimpleTest(SimpleTestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status.code, 200)
#
#     def test_view_member_page(self):
#         response = self.client.get('view_member/')
#         self.asserEqual(response.status.code, 200)