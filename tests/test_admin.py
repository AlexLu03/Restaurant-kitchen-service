from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Cook, DishType


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass'
        )
        self.client.force_login(self.admin_user)
        self.cook: Cook = Cook.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            years_of_experience=5,
            password='testpass'
        )

    def test_cook_years_of_experience_listed(self):
        url = reverse('admin:kitchen_cook_changelist')
        response = self.client.get(url)

        self.assertContains(response, str(self.cook.years_of_experience))

    def test_cook_year_of_experience_add(self):
        url = reverse('admin:kitchen_cook_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="years_of_experience"')

    def test_cook_years_of_experience_change(self):
        url = reverse(
            'admin:kitchen_cook_change',
            args=[self.cook.pk]
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="years_of_experience"')

    def test_dish_type_admin_searches_by_name(self):
        DishType.objects.create(name='Cake')
        DishType.objects.create(name='Soup')

        url = reverse('admin:kitchen_dishtype_changelist')
        response = self.client.get(url, {'q': 'Cake'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cake')
        result_names = [
            dish_type.name for dish_type in response.context['cl'].result_list
        ]
        self.assertEqual(result_names, ['Cake'])
