from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from core.models import UserProfessor, UserCandidate, User, File, Message
from core.fields import CommaSeparatedUserField
from django.utils.translation import ugettext_lazy as _
from core.helper_functions import contain_invalid_char


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'file',)


class EditFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('description', 'name',)

    def clean_name(self):
        data = self.cleaned_data['name']
        if contain_invalid_char(data):
            raise forms.ValidationError('The file name cannot contain the following characters: \\ / : * ? " < > |')
        return data


class UserForm(forms.ModelForm):
    """Although the user class in django has the
    password attribute.
    This is to overwrite it so it can hide the input."""
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'institution', 'self_website',)


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
    subject = forms.CharField(label=_(u"Subject"), max_length=70)
    body = forms.CharField(label=_(u"Body"),
                           widget=forms.Textarea(attrs={'rows': '12', 'cols': '55'}), max_length=250)
    file = forms.FileField(required=False)
    recipients = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)

    def save(self, sender,):
        recipients = self.cleaned_data['recipients']
        subject = self.cleaned_data['subject']
        body = self.cleaned_data['body']
        file = self.cleaned_data['file']
        message_list = []
        for r in recipients:
            message = Message(
                subject=subject,
                body=body,
                sender=sender,
                receiver=User.objects.get(username=r),
                file=file,
            )
            message.save()
            message_list.append(message)
        return message_list


class GroupForm(forms.Form):
    """
    A form which is used to create groups.
        def __init__(self, dataset=None, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        if dataset:
            self.fields['members'].choices = dataset

    """
    title = forms.CharField(required=True, max_length=70, label="The title of the group:")
    members = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple,
                                        label="Choose the members of the group:")


class AddGroupForm(forms.Form):
    """
    Add multiple groups to the recipients lists.
    """
    groups = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple,
                                       label="Choose the group:")


class RelationshipForm(forms.Form):
    """
    Define a form to add additional relation between candidates and professors.
    """
    username = forms.CharField(required=True, max_length=40,
                               label="Please input the email of the user you want to add:")
    description = forms.CharField(required=False, max_length=80, label="Include anything to prove your identity:")









