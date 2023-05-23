from django import forms


from django.contrib.auth.models import User

from .models import Profile, UserInfo, Post


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        exclude = {
            'first_name',
            'last_name',
            'email',
            'confirm_password'
        }
        widgets = {
            'password':forms.PasswordInput()
        }

    # def clean(self):
    #     cleaned_data = super().clean()

    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #     user = authenticate(username=username, password=password)

    #     return cleaned_data


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = UserInfo
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        widgets = {
            'password':forms.PasswordInput(),
            'confirm_password':forms.PasswordInput(),
            'email':forms.EmailInput()
        }
        labels = {
            'password':'Password',
            'confirm_password':'Confirm Password',
        }
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows':3}),
            'profile_picture': forms.FileInput(attrs={'id':'id_profile_picture'})
        }
        labels = {
            'bio': '',
            'profile_picture': 'Upload Image'
        }

class PostForm(forms.Form):
    post_input_text = forms.CharField(max_length=100, label='New Post')

class CommentForm(forms.Form):
    comment_input_text = forms.CharField(max_length=100, label='Comment')
    





