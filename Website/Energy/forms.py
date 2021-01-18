from django import forms
from .models import Observation
from .cleaner import cleaner
from django.forms import ClearableFileInput
from django.db import transaction
from django.core.validators import FileExtensionValidator

class ObservationForm(forms.Form):

    """
    Form that takes in and cleans uploaded data
    """

    file = forms.FileField(widget=ClearableFileInput(attrs={'multiple': True, 'accept': '.csv'}),
                           validators=[FileExtensionValidator(['csv'])])

    @transaction.atomic()
    def save(self, file):

        clean_data = cleaner(file)

        for building in clean_data:
            for index, obs in enumerate(clean_data[building]):
                Observation.objects.get_or_create(building=building,
                                                  Quantity=obs,
                                                  Time=clean_data.index[index])
            print("Saved {}.".format(building))


class InputForm(forms.Form):

    """
    Form that takes in names of buildings to be plotted.
    """

    building_names = ['Adams', 'Bertram', 'Carnegie', 'Chapel', 'Chase', 'Pettigrew', 'Rzasa', 'Libbey', 'Page',
                      'Rand', 'Schaeffer', 'Lane', 'Ladd', 'Hathorn', 'Parker', 'Cheney', 'Dana',
                      'Underhill', 'Underhill Ice', 'Olin', 'Pettengill']

    choices = [(x, x) for x in building_names]

    building = forms.CharField(widget=forms.CheckboxSelectMultiple(choices=choices))