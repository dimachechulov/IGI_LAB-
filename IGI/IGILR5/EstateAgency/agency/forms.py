

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User

from .models import *
from .utils import get_all_employees



class DateInput(forms.DateInput):
    input_type='date'

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Username', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'First Name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Last Name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'lf--input', 'placeholder': 'Email', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'lf--input', 'placeholder': 'Password', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'lf--input', 'placeholder': 'Repeat password', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    phone_number = forms.CharField(label='phone number', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'phone number', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    date = forms.DateField(label='Enter you birth day', widget=DateInput)
    photo = forms.ImageField(label='Image', required=False)
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password1', 'password2','date', 'phone_number', 'photo')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'lf--input', 'placeholder': 'Username', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'lf--input', 'placeholder':'Password', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))



class AdminAddRealtyForm(forms.ModelForm):
    name = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    description = forms.CharField(label='description', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'discription', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'lf--input', 'placeholder': 'price', 'min': '1',  'step': '1', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    photo = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label="Select category", queryset=Category.objects.all())
    state = forms.CharField(label='state', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'State',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    city = forms.CharField(label='city', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'City',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    address = forms.CharField(label='address', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Address',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))

    employee = forms.ModelChoiceField(label="Select employee", queryset=get_all_employees())
    class Meta:
        model = Realty
        fields = ('name', 'description','price','photo', 'category', 'employee')

class AddRealtyForm(forms.ModelForm):
    name = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    description = forms.CharField(label='description', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'discription', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'lf--input', 'placeholder': 'price', 'min': '1',  'step': '1', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    photo = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label="Select category", queryset=Category.objects.all())
    state = forms.CharField(label='state', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'State',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    city = forms.CharField(label='city', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'City',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    address = forms.CharField(label='address', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Address',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))

    class Meta:
        model = Realty
        fields = ('name', 'description','price','photo', 'category')

class AdminUpdateRealtyForm(forms.ModelForm):
    name = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    description = forms.CharField(label='description', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'description', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'lf--input', 'placeholder': 'price', 'min': '1',  'step': '1', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    photo = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label="Select category", queryset=Category.objects.all())
    state = forms.CharField(label='state', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'State',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    city = forms.CharField(label='city', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'City',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    address = forms.CharField(label='address', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Address',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))

    employee = forms.ModelChoiceField(label="Select employee", queryset=get_all_employees())
    class Meta:
        model = Realty
        fields = ('name', 'description','price','photo', 'category', 'employee')

class UpdateRealtyForm(forms.ModelForm):
    name = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    description = forms.CharField(label='description', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'description', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    price = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'lf--input', 'placeholder': 'price', 'min': '1',  'step': '1', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    photo = forms.ImageField(label='Image')
    category = forms.ModelChoiceField(label="Select category", queryset=Category.objects.all())
    state = forms.CharField(label='state', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'State',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    city = forms.CharField(label='city', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'City',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    address = forms.CharField(label='address', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Address',
               'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))

    class Meta:
        model = Realty
        fields = ('name', 'description','price','photo', 'category')

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(label='UserName', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Username', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'First Name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'Last Name', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'lf--input', 'placeholder': 'Email', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    phone_number = forms.CharField(label='phone number', widget=forms.TextInput(
        attrs={'class': 'lf--input', 'placeholder': 'phone number', 'style': 'width: 400px; text-align: center; border: 1px solid black; border-radius: 10px; height: 33px;'}))
    date = forms.DateField(label='Enter you birth day',widget=DateInput)
    photo = forms.ImageField(label='Image')
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'date', 'phone_number', 'photo')


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.NumberInput(attrs={'min': '1', 'max': '5', 'step': '1'}), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = Review
        fields = ('rating', 'text')