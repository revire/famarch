from django.urls import reverse, resolve


class TestUrls:

    def test_detail_url(self):
        path = reverse('view_member', kwargs={'slug':'hermann_hesse_1877-07-02-000000'})
        assert resolve(path).view_name =='view_member'

