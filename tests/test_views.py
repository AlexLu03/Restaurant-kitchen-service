from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from kitchen.forms import CookSearchForm
from kitchen.models import Cook, Dish, DishType


class ViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@test.com',
            password='testpass',
            years_of_experience=2
        )

    def test_index_page_open(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

    def test_correct_number_of_cooks(self):
        Cook.objects.create_user(
            username='testuser2',
            email='testuser2@test.com',
            password='testpass2',
            years_of_experience=3
        )

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['avaible_cooks'], 2)

    def test_cooks_list_search_by_login(self):
        self.client.force_login(self.user)
        other_user = get_user_model().objects.create_user(
            username='otheruser',
            email='otheruser@test.com',
            password='otherpass'
        )

        response = self.client.get(
            reverse('kitchen:cook-list'),
            {'username': 'otheruser'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, other_user.username)
        result_usernames = [
            cook.username for cook in response.context['cook_list']
        ]
        self.assertEqual(result_usernames, [other_user.username])

    def test_cooks_list_search_by_lowest_years_of_experience(self):
        self.client.force_login(self.user)
        qualified_user = Cook.objects.create_user(
            username='senior_cook',
            email='senior@test.com',
            password='pass',
            years_of_experience=5
        )
        junior_user = Cook.objects.create_user(
            username='junior_cook',
            email='junior@test.com',
            password='pass',
            years_of_experience=0
        )

        response = self.client.get(
            reverse('kitchen:cook-list'),
            {'min_experience': '2'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, qualified_user.username)
        self.assertContains(response, self.user.username)
        self.assertNotContains(response, junior_user.username)

    def test_cooks_list_search_by_highest_years_of_experience(self):
        self.client.force_login(self.user)
        senior_user = Cook.objects.create_user(
            username='senior_cook',
            email='senior@test.com',
            password='pass',
            years_of_experience=10
        )
        normal_user = Cook.objects.create_user(
            username='normal_cook',
            email='normal@test.com',
            password='pass',
            years_of_experience=5
        )

        response = self.client.get(
            reverse('kitchen:cook-list'),
            {'max_experience': '5'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
        self.assertContains(response, normal_user.username)
        self.assertNotContains(response, senior_user.username)

    def test_cook_create_view(self):
        self.client.force_login(self.user)
        form_data = {
            'username': 'new_cook',
            'first_name': 'New',
            'last_name': 'Cook',
            'email': 'new_cook@example.com',
            'years_of_experience': 3,
        }

        response = self.client.post(
            reverse('kitchen:cook-create'),
            data=form_data
        )

        self.assertRedirects(response, reverse('kitchen:cook-list'))
        self.assertTrue(Cook.objects.filter(username='new_cook').exists())

    def test_cook_search_filters(self):
        self.client.force_login(self.user)
        user_1 = Cook.objects.create_user(
            username='anna_junior',
            first_name='Anna',
            last_name='One',
            email='user_1@example.com',
            years_of_experience=1
        )
        user_2 = Cook.objects.create_user(
            username='anna_senior',
            first_name='Anna',
            last_name='Two',
            email='user_2@example.com',
            years_of_experience=5
        )
        user_3 = Cook.objects.create_user(
            username='dan_senior',
            first_name='Dan',
            last_name='Three',
            email='user_3@example.com',
            years_of_experience=10
        )

        response = self.client.get(
            reverse('kitchen:cook-list'),
            {'username': 'anna', 'min_experience': 4}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user_2.username)
        self.assertNotContains(response, user_3.username)
        self.assertNotContains(response, user_1.username)

    def test_cook_list_includes_search_form(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('kitchen:cook-list'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['search_form'], CookSearchForm)

    def test_dish_create_view(self):
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name='Main Course')

        form_data = {
            'name': 'New Dish',
            'description': 'A delicious new dish.',
            'price': 9.99,
            'dish_type': dish_type.pk,
            'cooks': [self.user.pk],
        }

        response = self.client.post(
            reverse('kitchen:dish-create'),
            data=form_data
        )

        self.assertRedirects(response, reverse('kitchen:dish-list'))

        dish = Dish.objects.get(name='New Dish')

        self.assertTrue(
            dish.cooks.filter(username=self.user.username).exists()
        )

    def test_dish_assign_cook_change(self):
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name='Soft drink')
        dish = Dish.objects.create(
            name='Existing Dish',
            description='Refreshing drink',
            price='1.49',
            dish_type=dish_type,
        )
        dish.cooks.add(self.user)

        new_cook = Cook.objects.create_user(
            username='dan_senior',
            first_name='Dan',
            last_name='Three',
            email='user_3@example.com',
            years_of_experience=10,
        )
        form_data = {
            'name': dish.name,
            'description': dish.description,
            'price': '1.49',
            'dish_type': dish_type.pk,
            'cooks': [new_cook.pk],
        }

        response = self.client.post(
            reverse('kitchen:dish-update', args=[dish.pk]),
            data=form_data,
        )

        self.assertRedirects(response, reverse('kitchen:dish-list'))
        dish.refresh_from_db()
        self.assertTrue(dish.cooks.filter(pk=new_cook.pk).exists())
        self.assertFalse(dish.cooks.filter(pk=self.user.pk).exists())
