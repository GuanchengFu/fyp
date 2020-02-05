from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from core.models import UserProfessor, UserCandidate, User



class UserForm(forms.ModelForm):
	"""Although the user class in django has the 
	password attribute.
	This is to overwrite it so it can hide the input."""
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = get_user_model()
		fields = ('username', 'email', 'password', 'first_name', 'last_name')



class UserProfessorForm(forms.ModelForm):
	class Meta:
		model = UserProfessor
		fields = ('picture',)


class UserCandidateForm(forms.ModelForm):
	class Meta:
		model = UserCandidate

		"""
		As the user input the name, the professor's name should pop up, so that they 
		can choose the one they want to choose.
		"""
		#Whether to include the professor?
		fields = ('picture', 'professor',)