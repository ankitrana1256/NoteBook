from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.RegexField(widget=forms.PasswordInput,
                                 regex=r'[\w+]{8,}',
                                 label='New password',
                                 help_text="Must be strong!",
                                 error_messages={'required': "ASDASDA",
                                                 'invalid': "ZZZZZ"}
                                 )
    password2 = forms.RegexField(widget=forms.PasswordInput,
                                 regex=r'[\w+]{8,}',
                                 label='Re-enter password',
                                 )

    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user
