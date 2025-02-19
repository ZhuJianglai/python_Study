from django.test import TestCase
from sign.models import Event,Guest
# Create your tests here.

class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name='oneplus 3 event', status=True, limit=2000, address='shenzhen', start_time='2018-03-01 02:18:22')
        Guest.objects.create(id=2, event_id=1, realname='alen', phone='17620092448', email='alen@mail.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, "beijin")
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='17620092448')
        self.assertEqual(result.realname, 'alen')
        self.assertFalse(result.sign)
