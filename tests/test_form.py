from django.test import TestCase
from kitchen.forms import CookSearchForm


class CookSearchFormTest(TestCase):
    def test_empty_form_is_valid(self):
        form = CookSearchForm(data={
            'username': '',
            'min_experience': '',
            'max_experience': '',
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_accepts_valid_data(self):
        form = CookSearchForm(data={
            'username': 'ValidName',
            'min_experience': '1',
            'max_experience': '10',
        })

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['min_experience'], 1)
        self.assertEqual(form.cleaned_data['max_experience'], 10)

    def test_form_reject_invalid_data_in_min_experience(self):
        form = CookSearchForm(data={
            'username': '###',
            'min_experience': '-1',
            'max_experience': '10',
        })

        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('min_experience', form.errors)

    def test_form_reject_invalid_data_in_max_experience(self):
        form = CookSearchForm(data={
            'username': '###',
            'min_experience': '1',
            'max_experience': '-10',
        })

        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('max_experience', form.errors)

    def test_form_reject_non_int_experience(self):
        form = CookSearchForm(data={
            'username': '###',
            'min_experience': 'one',
            'max_experience': 'ten'
        })

        self.assertFalse(form.is_valid(), form.errors)
        self.assertIn('min_experience', form.errors)
        self.assertIn('max_experience', form.errors)
