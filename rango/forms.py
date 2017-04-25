from django import forms
from rango.models import Category, Subject, UserProfile, BaiduEditor
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the course name in English.")
    name_ch = forms.CharField(max_length=128, help_text="Please enter the course name in Chinese.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        #fields = ('name','name_ch',)
        exclude = ('subject',)		
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
		
class TestUeditorModelForm(forms.ModelForm):

    class Meta:
        model = BaiduEditor
        fields = ('content',)