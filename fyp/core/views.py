from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.forms import UserForm, UserProfessorForm, UserCandidateForm, IdentityForm, FileForm, editFileForm
from core.forms import sendMessageForm
from core.models import File
from django.core.files import File as File_Django
import os


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

            user = authenticate(email=email, password=password)

            if user:
                if user.is_active:

                    login(request, user)
                    return redirect('core:dashboard')
                else:
                    return HttpResponse("Your account is disabled.")
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
            return HttpResponseRedirect(reverse('core:proRegister'))
        else:
            return HttpResponseRedirect(reverse('core:canRegister'))
    else:
        return HttpResponse("Something goes wrong.")


def register(request):
    identity_form = IdentityForm()
    context_dictionary = {'identity_form': identity_form}
    return render(request, 'core/register-first-step.html', context_dictionary)


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

            return HttpResponse("Register successful!")

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

            registered = True

            return HttpResponse("Register successful!")

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


"""
This function will present the user information and files.
for reference:https://stackoverflow.com/questions/32033121/display-uploaded-files-django
显示pid？ 显示每个用户独一无二的一个数字
tango_with_django 的第101页
redirect to the user based on the id acquired from user.id?
"""


@login_required
def show_dashboard(request):
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
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        uploaded_file = request.FILES['file']
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            print(uploaded_file.name)
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





