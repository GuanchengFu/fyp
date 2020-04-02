from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    """
    A backend which is used to customising the authentication system.
    reference:
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/
    """
    def authenticate(self, request, email=None, password=None, key=None, **kwargs):
        """
        The key argument is used for staff login.
        """
        UserModel = get_user_model()
        try:
            if key is None:
                user = UserModel.objects.get(email=kwargs['username'])
            else:
                user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
