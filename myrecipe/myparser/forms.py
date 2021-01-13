from django import forms


class RecipeFinder(forms.Form):
    search = forms.CharField(required=True,
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Enter link or name of the recipe'
                             }))
