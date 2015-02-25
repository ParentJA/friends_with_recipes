__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class BootstrapMixin(object):
    def __init__(self, use_bootstrap=True, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        if use_bootstrap:
            for key in self.fields:
                self.fields[key].widget.attrs.update({
                    'class': 'form-control'
                })


class SignUpForm(BootstrapMixin, forms.ModelForm):
    error_messages = {
        'duplicate_email': 'A user with that email already exists.',
        'password_mismatch': 'The two password fields didn\'t match.'
    }

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput,
        help_text='Enter your password again.'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        authenticated_user = authenticate(username=user.username, password=self.cleaned_data['password1'])

        return authenticated_user


class LogInForm(BootstrapMixin, AuthenticationForm):
    pass


class ProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ('photo', 'date_of_birth', 'address', 'phone_number')
        widgets = {
            'date_of_birth': forms.fields.TextInput(attrs={
                'placeholder': 'i.e. 6/2/1979',
                'type': 'date'
            }),
            'address': forms.fields.TextInput(attrs={
                'placeholder': 'i.e. 6586 Bollinger Rd'
            }),
            'phone_number': forms.fields.TextInput(attrs={
                'placeholder': 'i.e. (913) 149-4498',
                'type': 'tel'
            })
        }