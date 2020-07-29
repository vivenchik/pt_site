from django import forms
from .models import Profile, Document
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class MomentFormDetails(forms.Form):
    details = forms.CharField()


class MomentFormImage(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        data = self.cleaned_data['image']
        # TODO warning
        return data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',
                  'phone',
                  'telegram',
                  'bank_account',
                  'location',
                  'birth_date',
                  'second_email',)

    def clean_telegram(self):
        data = self.cleaned_data['telegram']

        if len(data) == 0 or data[0] != '@':
            raise ValidationError(_('telegram must start with @'))

        return data


class DocumentForm(forms.Form):
    name = forms.CharField()
    file = forms.FileField()
