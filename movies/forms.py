import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import requests
import os

class AddMovieForm(forms.Form):
    name = forms.CharField(help_text="Enter the name of the movie",required=True)

    #Verify if the movie actually exist
    def clean_name(self):
        name = self.cleaned_data['name']

        key = os.environ.get('API_KEY')

        url = f'http://www.omdbapi.com/?apikey={key}&t={name}'

        data = requests.get(url)

        data2 = data.json()

        #If the movie does not exist, raise an error
        if data2["Response"]=="False":
            raise ValidationError(_('Invalid title - Movie does not exist'))

        return name

