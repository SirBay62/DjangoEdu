from django import forms
from django.core import validators
from shopapp.models import Product

from django.contrib.auth.models import Group
from django.forms import ModelForm


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value = 100000)
#     description = forms.CharField(
#         label = 'Product description',
#         widget=forms.Textarea(attrs={'rows':10, 'cols':50}),
#         validators=[validators.RegexValidator(
#            regex=r'great',
#            message="Product description must contain word 'great'."
#         )]
#     )

class GroupsForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ='name', 'price', 'description', 'discount'

