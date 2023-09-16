from django import forms
from django.contrib.auth.models import User
from Library.models import Book
from . import models

class IssueBookForm(forms.Form):
    fees2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), empty_label="Book Name [Fees]", to_field_name="fees", label="Book (Name and Fees)")

    name2 = forms.ModelChoiceField(queryset=models.Member.objects.all(), empty_label="Name [Phone]", to_field_name="user", label="Member Details")
    
    
    fees2.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})


class BookForm(forms.ModelForm):  
    class Meta:  
        model = Book 
        fields = ['name', 'author', 'fees', 'quantity'] 
        widgets = { 'name': forms.TextInput(attrs={ 'class': 'form-control' }), 
            'author': forms.EmailInput(attrs={ 'class': 'form-control' }),
            'fees': forms.TextInput(attrs={ 'class': 'form-control' }),
            'quantity': forms.TextInput(attrs={ 'class': 'form-control' }),

      }




