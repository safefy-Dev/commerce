from django import forms
from .models import Listings,Watchlists,Comment

CATEGORY_CHOICES = [
    ("Fashion", "Fashion"),
    ("Toys", "Toys"),
    ("Electronics", "Electronics"),
    ("Home", "Home"),
    ("Other", "Other"),
]
class Listings_Form(forms.Form):
    title = forms.CharField(label='Title', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control'}))
    starting_bid = forms.DecimalField(label='Starting Bid', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image_url = forms.URLField(label='Image URL', required=False, widget=forms.URLInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(label='Category', choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))

class Biding_form(forms.Form):
    starting_bid = forms.DecimalField(label='Bid', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class Watchlist_form(forms.Form):
    class Meta:
        model = Watchlists
        fields = []

class close_form(forms.Form):
    class Meta:
        model = Listings
        fields = []

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }