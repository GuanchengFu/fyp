from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.forms import UserForm, UserProfessorForm, UserCandidateForm, IdentityForm, DisplayIdentityForm

"""Index page for the website"""


def index(request):
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
        # identity_form = IdentityForm()
        # context_dictionary = {'identity_form': identity_form}
        return render(request, 'core/index-new-new.html')


def about(request):
    return HttpResponse("Write something about the website later.")


def redirected(request):
    if request.method == 'POST':
        identity = request.POST.get('identity')

        if identity == "professor":
            # return redirect(reverse('core:proRegister'))
            return HttpResponseRedirect(reverse('core:proRegister'))
        else:
            return HttpResponseRedirect(reverse('core:canRegister'))
    else:
        return HttpResponse("Something goes wrong.")


def register(request):
    identity_form = IdentityForm()
    context_dictionary = {'identity_form': identity_form}
    return render(request, 'core/register-first-step.html', context_dictionary)


def professorRegister(request):
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


def candidateRegister(request):
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
        content = {}
        # The user should have logged in based on the decorator @login_required
        user = request.user
        if user.is_professor:
            return HttpResponse("Try this one, professor!")
        elif user.is_candidate:
            return HttpResponse("Candidate, this really works!")
        else:
            return HttpResponse("You are a staff of this website, try using this site for logging in.")
