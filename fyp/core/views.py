from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from core.forms import UserForm, UserProfessorForm, UserCandidateForm, IdentityForm, FileForm, editFileForm
from core.forms import sendMessageForm, ComposeForm, GroupForm, AddGroupForm
from core.helper_functions import generate_time_prefix
from core.models import File, Message, Group
from django.core.files import File as File_Django
import os
from django.utils import timezone

User = get_user_model()


def index(request):
    """
    A index page for the website.
    Redirect to the dashboard if the user logged in.
    Otherwise, let the user login use the email and password.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(email=email, password=password, key="UserLogIn")

            if user:
                # Only log the user in if he is not one of the staffs.
                if user.is_candidate or user.is_professor:
                    login(request, user)
                    return redirect('core:dashboard')
                else:
                    return HttpResponse("You are a staff of this website, try using another site for logging in.")
            else:
                # Bad login details are provided.  The user cannot login.
                print("Invalid login details: {0}, {1}".format(email, password))
                return HttpResponse("Invalid login details supplied.")
        else:
            return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def redirected(request):
    """
    A middle function to dispose the sign up identification.
    """
    if request.method == 'POST':
        identity = request.POST.get('identity')

        if identity == "professor":
            return redirect(reverse('core:proRegister'))
        else:
            return redirect(reverse('core:canRegister'))
    else:
        return HttpResponse("Something goes wrong.")


def register(request):
    """
    The first step of the registration, which require the user to select their identification.
    """
    identity_form = IdentityForm()
    context_dictionary = {'identity_form': identity_form}
    return render(request, 'core/registration_first_step.html', context_dictionary)


def professor_register(request):
    """
    The function to dispose the sign up detail for a professor.
    """
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfessorForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.is_professor = True
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

            new_user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'],
                                    key="UserLogIn")

            login(request, new_user)

            return redirect(reverse('core:dashboard'))

        else:
            print(user_form.errors, profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = UserProfessorForm()

    return render(request,
                  'core/professor_registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def candidate_register(request):
    """
    A function to dispose the sign up detail for a candidate.
    """
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserCandidateForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.is_candidate = True
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            """
            Reference for using this:
            https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
            """
            profile_form.save_m2m()

            registered = True

            new_user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'],
                                    key="UserLogIn")

            login(request, new_user)

            return redirect(reverse('core:dashboard'))

        else:
            print(user_form.errors, profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = UserCandidateForm()

    return render(request,
                  'core/candidate_registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))


@login_required
def show_dashboard(request):
    """
    Show the dashboard of the user.
    """
    if request.method == 'GET':
        context = {}
        # The user should have logged in based on the decorator @login_required
        user = request.user
        context['user'] = user
        context['files'] = user.userfiles.all()
        if user.is_professor:
            profile = user.professor
            context['profile'] = profile
            # Later change this so that a professor and a candidate will have a different view based on their identity.
            return render(request, 'core/dashboard.html', context)
        elif user.is_candidate:
            profile = user.candidate
            context['profile'] = profile
            return render(request, 'core/dashboard.html', context)
        else:
            return HttpResponse("You are a staff of this website, try using this site for logging in.")


@login_required
def upload_file(request):
    """
    A view to let the user upload the file.
    The uploaded file will be saved as a File object.
    user: request.user
    description: Uploaded in the form.
    file: Uploaded in the form.
    name: Will be auto recorded as the file name.
    This can lead to FileExistError.
    created: Auto created.
    modified: When the description or the name of the file is changed.
    """
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)

        # An instance of class UploadedFile
        uploaded_file = request.FILES['file']
        if form.is_valid():
            # file is the File object while the uploaded_file is the file object.
            file = form.save(commit=False)
            file.user = request.user
            # upload_file.name is only the name of the file, rather than the path.
            # "test.txt for example."
            file.name = uploaded_file.name
            file.save()
            return redirect('core:dashboard')
        else:
            print(form.errors)
    else:
        form = FileForm()
        return render(request, 'core/upload_file.html', {
            'form': form,
        })


# Possible reference: https://stackoverflow.com/questions/604266/django-set-default-form-values
# for the default values in the django form.
# Possible reference: https://stackoverflow.com/questions/39919012/django-python-show-pdf-in-a-template
# to have a preview in the page.
# For pop up forms:
# https://stackoverflow.com/questions/52501470/i-want-to-create-django-popup-form-in-my-project/52501740
# Use the modals:
# https://getbootstrap.com/docs/4.2/components/modal/


@login_required
def edit_file(request, file_id):
    context = {}
    user = request.user
    try:
        file = File.objects.get(id=file_id)
        context['file'] = file
    except File.DoesNotExist:
        context['file'] = None

    if request.method == "POST":
        form = editFileForm(request.POST, instance=file)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = editFileForm(instance=file)
    context['form'] = form
    share_form = sendMessageForm(initial={'file': file.file})
    context['share_form'] = share_form
    return render(request, 'core/edit-file.html', context)


def delete_file(request, file_id):
    file = File.objects.get(id=file_id)
    file.delete()
    return redirect('core:dashboard')


def filename(s):
    """
    Return the filename from a path.
    Reference:
    https://stackoverflow.com/questions/2683621/django-filefield-how-to-return-filename-only-in-template
    """
    return os.path.basename(s)


@login_required
def dispose_message_form(request, file_id):
    """
    Dispose the modal share button.
    Reference:
    https://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
    https://docs.djangoproject.com/en/3.0/ref/unicode/
    The above website gives an idea that we should use the UTF-8 as the default encoding for
    Python.
    The problem is that the file 
    """
    if request.method == "POST":
        file = File.objects.get(id=file_id)
        # The open method requires the absolute path.
        f = open(file.file.path, mode="rb")
        share_file = File_Django(f)
        form = sendMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = request.user.candidate.professor.user
            """
            The save method requires two arguments:
            1.name which is the name of the file.
            2.content which is an object containing the file’s contents (an instance of django.core.files.File)
            """
            message.file.save(filename(share_file.name), share_file)
            message.save()
            return HttpResponse("Message created successfully!")
        else:
            print(form.errors)


@login_required
def show_message(request):
    """
    Show all the messages received by the user.
    previous version:
    if request.method == "GET":
        context = {}
        user = request.user
        context['user'] = request.user
        context['messages'] = user.received_messages.order_by('-sent_at')
        return render(request, 'core/show_messages.html', context)
    """
    message_list = Message.objects.inbox_for(request.user)
    return render(request, 'core/show_messages.html', {'messages': message_list, })


@login_required
def check_message(request, message_id):
    """
    Check Each message.
    Implement later.
    """


@login_required
def outbox(request,):
    message_list = Message.objects.outbox_for(request.user)
    return render(request, 'core/outbox.html', {'message_list': message_list})


@login_required
def trash(request,):
    message_list = Message.objects.trash_for(request.user)
    return render(request, 'core/trash.html', {'message_list': message_list})


@login_required
def connection(request,):
    """
    Show all the connections with other professors.
    Display the groups that the student was enrolled in.
    Should display different pages for different users.
    The form doesn't add the user into its
    """
    user = request.user
    context_dict = {}
    if user.is_professor:
        # User is professor, acquire all his candidates and groups into the context_dict.
        candidates = user.professor.students.all()
        context_dict['candidates'] = candidates
        context_dict['collaborated_professors'] = user.professor.collaborated_professors.all()

        # Acquire all the groups created by the professor.
        group_created = user.professor.created_groups.all()
        context_dict['created_groups'] = group_created
        return render(request, 'core/connection.html', context_dict)
    elif user.is_candidate:
        professors = user.candidate.professor.all()
        context_dict['professors'] = professors
        return render(request, 'core/connection.html', context_dict)


def get_related_candidates(user):
    """
    Return a list with all the related students for a professor.
    user: A professor's user object.
    """
    result = []
    students = user.professor.students.all()
    for student in students:
        result.append((student.user.username, student.user.username))
    return result


def get_related_professors(user):
    """
    Return a list with all the related professors for a candidates.
    user: A user candidate.
    """
    result = []
    professors = user.candidate.professor.all()
    for professor in professors:
        result.append((professor.user.username, professor.user.username))
    return result


def get_collaborated_professors(user):
    result = []
    professors = user.professor.collaborated_professors.all()
    for professor in professors:
        result.append((professor.user.username, professor.user.username))
    return result


def get_related_groups(user):
    """
    Return a list with all the groups created by a certain professor.
    """
    result = []
    groups = Group.objects.filter(creator=user.professor)
    for group in groups:
        result.append((group.id, group.title))
    return result


@login_required
def create_group(request,):
    """
    Create group for the professor user.
    """
    if request.method == "GET":
        form = GroupForm()
        # Set the choices field for the member fields.
        form.fields['members'].choices = get_related_candidates(request.user)
        return render(request, 'core/create_group.html',
                      {'form': form, })
    # The request is a POST method.
    elif request.method == "POST":
        """
        We need to set the choices field for the form, so that it can validates itself.
        """
        form = GroupForm(request.POST)
        form.fields['members'].choices = get_related_candidates(request.user)
        if form.is_valid():
            members = form.cleaned_data['members']
            title = form.cleaned_data['title']
            group = Group()
            group.creator = request.user.professor
            group.title = title
            group.save()
            for student in members:
                candidate = User.objects.get(username=student).candidate
                group.members.add(candidate)
            return redirect("core:connection")
        else:
            print(form.errors)


def send_message(request,):
    """
    The view to allow the user to send messages to other users.
    This is not the same to reply message.
    """
    user = request.user
    context_dict = {}
    if request.method == "POST":
        sender = user
        message_form = ComposeForm(request.POST, request.FILES)
        if user.is_professor:
            choices = get_related_candidates(user) + get_collaborated_professors(user)
            group_form = AddGroupForm(request.POST)
            group_form.fields['groups'].choices = get_related_groups(user)
            message_form.fields['recipients'].choices = choices

            if message_form.is_valid() and group_form.is_valid():
                groups = group_form.cleaned_data['groups']
                recipients = message_form.cleaned_data['recipients']
                if groups or recipients:
                    """
                    Have recipients, the form should be saved.
                    """
                    if groups:
                        for group in groups:
                            g = Group.objects.get(id=group)
                            for u in g.members.all():
                                if u not in recipients:
                                    recipients.append(u)
                    message_form.fields['recipients'] = recipients
                    message_form.save(request.user)
                    return redirect('core:outbox')
            else:
                print(message_form.errors, group_form.errors)
        elif user.is_candidate:
            choices = get_related_professors(user)
            message_form.fields['recipients'].choices = choices
            if message_form.is_valid():
                message_form.save(user)
                return redirect('core:outbox')

    else:
        form_message = ComposeForm()
        if user.is_professor:
            choices = get_related_candidates(user) + get_collaborated_professors(user)
            form_group = AddGroupForm()
            form_group.fields['groups'].choices = get_related_groups(request.user)
            context_dict['form_group'] = form_group
        elif user.is_candidate:
            choices = get_related_professors(user)
            context_dict['form_group'] = None

        form_message.fields['recipients'].choices = choices
        context_dict['form_message'] = form_message

    return render(request, 'core/send_message.html', context_dict)


@login_required
def view_message(request, message_id):
    """
    Show a single message.
    message_id: The id of the message in the database.
    May need to distinguish between reply message or send message.
    Should include a upload_file form if the user wants to upload the attached files into their system.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.receiver != user):
        raise Http404
    if message.is_read is False and message.receiver == user:
        message.is_read = True
        message.save()
    context = {'message': message, 'reply_form': None}
    if message.file:
        """
        Allow the user to save the file included in the message.
        """
        save_form = FileForm(initial={'file': message.file})
        context['save_form'] = save_form
        context['file'] = message.file
    else:
        context['save_form'] = None
    return render(request, 'core/view_message.html', context)
    # May need to give a form for replying the message.


@login_required
def save_file(request, message_id):
    """
    Save the file which is included in the message.
    Two different conditions:
    1. The user has changed the file, which is included in the request.FILES
    2. The original file is uploaded.
    """
    user = request.user
    message = get_object_or_404(Message, id=message_id)
    if (message.sender != user) and (message.receiver != user):
        raise Http404
    if request.method == "POST":
        # First condition:
        if 'file' in request.FILES:
            form = FileForm(request.POST, request.FILES)
            file = request.FILES['file']
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.user = user
                save_form.name = file.name
                save_form.save()
                return redirect('core:dashboard')
            else:
                print(form.errors)
        else:
            # Second condition.
            form = FileForm(request.POST, request.FILES)
            file = message.file
            f = open(file.path, mode='rb')
            file_django = File_Django(f)
            file_object = File()

            file_object.created = timezone.now()

            file_object.description = request.POST['description']
            file_object.name = filename(file.name)
            file_object.user = user
            """
            This can lead to the change in file name.  
            For instance: It might be the case that the user already has a file with the name 
            file.name.
            """
            file_object.file.save(filename(file_django.name), file_django)
            file_object.save()
            return redirect('core:dashboard')
    else:
        raise Http404





