from django import forms
from .models import Post, Category, User, Comment
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author','created_date','published_date',)


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = User
        fields = ['user_img','username','first_name','last_name','password1','password2','email','phone_no','gender','date_of_birth','company','city','state','country','user_web','user_address','rule']        

class LoginForm(forms.Form):
    username = forms.CharField(label='Please Enter email or username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','comment_content')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_img','first_name', 'email', 'gender', 'date_of_birth', 'phone_no', 'city', 'state', 'country']