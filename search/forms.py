from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for posts...',
            'aria-label': 'Search',
            'autocomplete': 'off',
        })
    )
