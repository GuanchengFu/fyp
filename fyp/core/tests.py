from django.test import TestCase
from core.forms import IdentityForm

# Create your tests here.


class IdentityFormTestCase(TestCase):
	
	def test_choice_valid(self):
		data = {'identity': 'candidate'}
		identity_form = IdentityForm(data = data)
		self.assertTrue(identity_form.is_valid())
		self.assertEqual(identity_form.cleaned_data['identity'], 'candidate')