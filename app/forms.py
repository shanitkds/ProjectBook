from django import forms
from .models import Book
from  django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User



class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=['name','auther','price','description','cover']
        
class CustomUseRCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
class LoginForm(AuthenticationForm):
    pass

