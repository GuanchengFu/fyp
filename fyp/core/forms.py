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

IDENTITY_CHOICES = [
	('professor', 'Professor'),
	('candidate', 'Candidate'),
]
"""
This form includes an additional attribute known as:
@arg identity to help the server decide the identity of the user.
"""
class RegisterUserForm(UserForm):
	identity = forms.CharField(label = 'What is your identity?', 
		widget = forms.Select(choices = IDENTITY_CHOICES))
	class Meta(UserForm.Meta):
		fields = UserForm.Meta.fields + ('identity',)



class UserProfessorForm(forms.ModelForm):
	#identity = forms.CharField(label = 'Your identity:', initial='Professor', disabled = True)
	class Meta:
		model = UserProfessor
		fields = ('picture',)


class UserCandidateForm(forms.ModelForm):
	#identity = forms.CharField(label = 'Your identity:', initial='Candidate', disabled = True)
	class Meta:
		model = UserCandidate

		"""
		As the user input the name, the professor's name should pop up, so that they 
		can choose the one they want to choose.
		"""
		#Whether to include the professor?
		fields = ('picture', 'professor',)




""""""
class IdentityForm(forms.Form):
	identity = forms.CharField(label = 'What is your identity?', 
		widget = forms.Select(choices = IDENTITY_CHOICES))


class DisplayIdentityForm(forms.Form):
	identity = forms.CharField()



