from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", 'password1', 'password2')
