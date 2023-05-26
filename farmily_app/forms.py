from django import forms
from .models import *
  
class ProductForm(forms.ModelForm):
    Choises = (("Fruits", "Фрукты"), ("Vegetables", "Овощи"), ("Pastry", "Выпечка"), ("Meat", "Мясные продукты"), ("Dairy", "Молочные продукты"))
    category = forms.ChoiceField(choices=Choises)
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price', 'category']
