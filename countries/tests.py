from django.test import TestCase
from django.contrib.auth.models import User
from .models import Country, CountryEntry
from rest_framework.test import APIClient
from rest_framework import status
from users.models import APIKey
from .models import Photo,Region, TravelItem


class CountryEntrySecurityTest(TestCase):

    def setUp(self):
        # User 1
        self.user1 = User.objects.create_user(
            username='user1',
            password='testpass'
        )
        self.api_key1 = APIKey.objects.create(
            user=self.user1,
            name='test-key-1'
        )

        # User 2
        self.user2 = User.objects.create_user(
            username='user2',
            password='testpass'
        )
        self.api_key2 = APIKey.objects.create(
            user=self.user2,
            name='test-key-2'
        )

        self.country = Country.objects.create(
            name='Japan',
            iso_code='JP',
            continent='AS',
            numeric_code='392'
        )

        # Entry belongs to user1
        self.entry = CountryEntry.objects.create(
            country=self.country,
            status='visited',
            user=self.user1
        )

        # Client authenticated as user2
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key2.key}')

    def test_user_cannot_see_other_users_countries(self):
        response = self.api_client.get('/api/my-countries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # user2 sees empty list

    def test_user_cannot_delete_other_users_entry(self):
        response = self.api_client.delete(f'/api/my-countries/{self.entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_request_is_rejected(self):
        client = APIClient()  # no credentials
        response = client.get('/api/my-countries/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
class CountryEntryModelTest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.api_key = APIKey.objects.create(
            user=self.user,
            name='test-key'
        )
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key.key}')
        self.country = Country.objects.create(
            name='Japan',
            iso_code='JP',
            continent='AS',
            numeric_code='392'
        )
        self.entry = CountryEntry.objects.create(
            country=self.country,
            status='visited',
            user=self.user
        )

    def test_entry_created(self):
        self.assertEqual(self.entry.status, 'visited')
        self.assertEqual(self.entry.country.name, 'Japan')

    def test_entry_str(self):
        self.assertIsNotNone(str(self.entry))

    def test_get_my_countries(self):
        response = self.api_client.get('/api/my-countries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_my_countries_returns_correct_country(self):
        response = self.api_client.get('/api/my-countries/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['country']['name'], 'Japan')

    def test_get_my_countries_returns_correct_status(self):
        response = self.api_client.get('/api/my-countries/')
        self.assertEqual(response.data[0]['status'], 'visited')

    def test_stats_returns_correct_visited_count(self):
        response = self.api_client.get('/api/my-countries/stats/')
        self.assertEqual(response.data['visited'], 1)

    def test_create_country_entry(self):
        country2 = Country.objects.create(
            name='Argentina',
            iso_code='AR',
            continent='SA',
            numeric_code='032'
        )
        response = self.api_client.post('/api/my-countries/', {
            'country_id': country2.id,
            'status': 'want_to_visit'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_country_entry(self):
        response = self.api_client.delete(f'/api/my-countries/{self.entry.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
class PhotoAPITest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass'
        )
        self.api_key = APIKey.objects.create(
            user=self.user,
            name='test-key'
        )
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key.key}')
        self.country = Country.objects.create(
            name='Japan',
            iso_code='JP',
            continent='AS',
            numeric_code='392'
        )
        self.entry = CountryEntry.objects.create(
            country=self.country,
            status='visited',
            user=self.user
        )
        self.photo = Photo.objects.create(
            country_entry=self.entry,
            title='Tokyo Tower',
            image_key='photos/test-uuid.jpeg'
        )

    def test_get_photos(self):
        response = self.api_client.get('/api/photos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_photos_returns_list(self):
        response = self.api_client.get('/api/photos/')
        self.assertIsInstance(response.data, list)

    def test_get_photos_returns_correct_title(self):
        response = self.api_client.get('/api/photos/')
        self.assertEqual(response.data[0]['title'], 'Tokyo Tower')

    def test_get_photos_filtered_by_country(self):
        response = self.api_client.get(f'/api/photos/?country_entry={self.entry.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_photo(self):
        response = self.api_client.delete(f'/api/photos/{self.photo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
class RegionAPITest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username='testuser_region',
            password='testpass'
        )
        self.api_key = APIKey.objects.create(
            user=self.user,
            name='test-key'
        )
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key.key}')
        self.country = Country.objects.create(
            name='Japan',
            iso_code='JP',
            continent='AS',
            numeric_code='392'
        )
        self.entry = CountryEntry.objects.create(
            country=self.country,
            status='visited',
            user=self.user
        )
        self.region = Region.objects.create(
            country_entry=self.entry,
            name='Tokyo',
            type='city'
        )

    def test_get_regions(self):
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/regions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_regions_returns_correct_name(self):
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/regions/')
        self.assertEqual(response.data[0]['name'], 'Tokyo')

    def test_create_region(self):
        response = self.api_client.post(f'/api/my-countries/{self.entry.id}/regions/', {
            'name': 'Kyoto',
            'type': 'city'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_region(self):
        response = self.api_client.delete(f'/api/regions/{self.region.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_region_count_after_create(self):
        self.api_client.post(f'/api/my-countries/{self.entry.id}/regions/', {
            'name': 'Osaka',
            'type': 'city'
        })
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/regions/')
        self.assertEqual(len(response.data), 2)


class TravelItemAPITest(TestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user = User.objects.create_user(
            username='testuser_item',
            password='testpass'
        )
        self.api_key = APIKey.objects.create(
            user=self.user,
            name='test-key'
        )
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Api-Key {self.api_key.key}')
        self.country = Country.objects.create(
            name='Japan',
            iso_code='JP',
            continent='AS',
            numeric_code='392'
        )
        self.entry = CountryEntry.objects.create(
            country=self.country,
            status='visited',
            user=self.user
        )
        self.item = TravelItem.objects.create(
            country_entry=self.entry,
            name='Senso-ji Temple',
            category='landmark',
            is_done=False
        )

    def test_get_items(self):
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_items_returns_correct_name(self):
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/items/')
        self.assertEqual(response.data[0]['name'], 'Senso-ji Temple')

    def test_create_item(self):
        response = self.api_client.post(f'/api/my-countries/{self.entry.id}/items/', {
            'name': 'Ramen at Ichiran',
            'category': 'food',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_is_done_defaults_to_false(self):
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/items/')
        self.assertEqual(response.data[0]['is_done'], False)

    def test_update_item_is_done(self):
        response = self.api_client.patch(f'/api/items/{self.item.id}/', {
            'is_done': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_done'], True)

    def test_delete_item(self):
        response = self.api_client.delete(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_item_count_after_create(self):
        self.api_client.post(f'/api/my-countries/{self.entry.id}/items/', {
            'name': 'Tokyo Tower',
            'category': 'landmark',
        })
        response = self.api_client.get(f'/api/my-countries/{self.entry.id}/items/')
        self.assertEqual(len(response.data), 2)
