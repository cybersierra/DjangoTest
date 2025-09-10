from django import forms
from .models import Entry
from datetime import date

# this will contain the forms for loggin in, entering giveaways, etc.

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['phone_number', 'date_of_birth']  # only ask for phone number and date of birth

        # validation
        def clean_date_of_birth(self):
            dob = self.cleaned_data['data_of_birth']
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise forms.ValidationError("You must be at least 18 years old to enter this giveaway.")
            return dob