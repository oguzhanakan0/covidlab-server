from django.test import TestCase

# Create your tests here.

# Create your tests here.

from labtest.models import Location


class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create(name="CovidLab San Diego",
                                slug="sandiego", longitude=1, latitude=1,
                                email="sandiego@covidlab.com")

    def test_location_string(self):
        loc = Location.objects.get(slug="sandiego")
        self.assertEqual(str(loc), 'sandiego')
