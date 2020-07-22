from django import forms


class MomentFormDetails(forms.Form):
    details = forms.CharField()


class MomentFormImage(forms.Form):
    image = forms.ImageField()

    def clean_image(self):
        data = self.cleaned_data['image']
        # TODO warning
        return data
