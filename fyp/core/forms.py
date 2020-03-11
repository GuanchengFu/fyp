from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from core.models import UserProfessor, UserCandidate, User, File, Message
from core.fields import CommaSeparatedUserField
from django.utils.translation import ugettext_lazy as _
class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'file',)


class editFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'name',)


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


class RegisterUserForm(UserForm):
    """
    This form includes an additional attribute known as:
    @arg identity to help the server decide the identity of the user.
	"""
    identity = forms.CharField(label='What is your identity?',
                               widget=forms.Select(choices=IDENTITY_CHOICES))

    class Meta(UserForm.Meta):
        fields = UserForm.Meta.fields + ('identity',)


class sendMessageForm(forms.ModelForm):
    """
    This form is only used in the share method within the edit-file.
    """

    class Meta:
        model = Message
        fields = ('subject', 'body', 'file')


class UserProfessorForm(forms.ModelForm):
    # identity = forms.CharField(label = 'Your identity:', initial='Professor', disabled = True)
    class Meta:
        model = UserProfessor
        fields = ('picture',)


class UserCandidateForm(forms.ModelForm):
    """
    As the user input the name, the professor's name should pop up, so that they
    can choose the one they want to choose.
    """
    # identity = forms.CharField(label = 'Your identity:', initial='Candidate', disabled = True)
    class Meta:
        model = UserCandidate
    # Whether to include the professor?
        fields = ('picture', 'professor',)


class IdentityForm(forms.Form):
    identity = forms.CharField(label='What is your identity?',
                               widget=forms.Select(choices=IDENTITY_CHOICES))


class DisplayIdentityForm(forms.Form):
    identity = forms.CharField()


class ComposeForm(forms.Form):
    """
    A form which is used to compose the Message class.
    Later add support to allow the user to choose the file within the system.
    This might have problems.
    recipient_filter: a function which receives a user object and returns a boolean
                     whether it is an allowed recipient or not.
    """
    recipient = CommaSeparatedUserField(label=_(u"Recipient"))
    subject = forms.CharField(label=_(u"Subject"), max_length=140)
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '12', 'cols': '55'}))
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        recipient_filter = kwargs.pop('recipient_filter', None)
        super(ComposeForm, self).__init__(*args, **kwargs)
        if recipient_filter is not None:
            self.fields['recipient']._recipient_filter = recipient_filter

    def save(self, sender, parent_msg=None):
        recipients = self.cleaned_data['recipient']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        file = self.cleaned_data['file']
        message_list = []
        for r in recipients:
            msg = Message(
                sender=sender,
                receiver=r,
                subject=subject,
                body=body,
                file=file,
            )
            if parent_msg is not None:
                msg.parent_msg = parent_msg
                parent_msg.save()
            msg.save()
            message_list.append(msg)
        return message_list

