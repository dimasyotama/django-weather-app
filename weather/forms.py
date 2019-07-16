from django.forms import ModelForm, TextInput
from .models import city

class CityForm(ModelForm):
    class Meta:
        model = city
        fields = ['name']
        widgets = {
            'name':TextInput(attrs={'class' : 'input','placholder' : 'City Name'})
        }