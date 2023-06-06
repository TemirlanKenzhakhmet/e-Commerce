from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



from .models import Item

KLASS = 'w-full py-4 px-6 rounded-xl border'
KLASS2 = 'w-3/4 py-2 px-3 rounded-xl border'


class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': KLASS
            }),
            'name': forms.TextInput(attrs={
                'class': KLASS
            }),
            'description': forms.Textarea(attrs={
                'class': KLASS
            }),
            'price': forms.TextInput(attrs={
                'class': KLASS
            }),
            'image': forms.FileInput(attrs={
                'class': KLASS
            }),
        }


class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': KLASS
            }),
            'description': forms.Textarea(attrs={
                'class': KLASS
            }),
            'price': forms.TextInput(attrs={
                'class': KLASS
            }),
            'image': forms.FileInput(attrs={
                'class': KLASS
            }),
        }

PAYMENT_OPTIONS = [
    ('S', 'Stripe'),
    ('P', 'Paypal'),
]

class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': KLASS2,
        'placeholder': "1234 Main St"
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': KLASS2,
        'placeholder': "Apartment or suite"
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': KLASS2
        })
    )
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': KLASS2}))
    same_shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': "w-4 h-4"
    }))
    save_info = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': "w-4 h-4"
    }))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTIONS)