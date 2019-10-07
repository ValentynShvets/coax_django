from django.contrib.auth.forms import UserCreationForm
from django.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        widgets = {

            'email': TextInput(attrs={'placeholder': "Email", 'class': 'form-control'}),

                   }

    User._meta.get_field('email')._unique = True

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': "Пароль", 'class': 'form-control'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': "Підтвердження пароля", 'class': 'form-control'})
