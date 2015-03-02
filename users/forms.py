__author__ = 'jason.parent@carneylabs.com (Jason Parent)'

# Django imports...
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class BootstrapMixin(object):
    def __init__(self, use_bootstrap=True, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)

        if use_bootstrap:
            for key in self.fields:
                self.fields[key].widget.attrs.update({
                    'class': 'form-control'
                })


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