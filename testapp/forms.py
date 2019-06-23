from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from testapp.models import Group, Comment, Classes, TimeChoice, Questions


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30, min_length=8, widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'password')


class SignUpForm(UserCreationForm):
    level = forms.ChoiceField(choices=[("Sec 1", "Sec 1"),
                                       ("Sec 2", "Sec 2"),
                                       ("Sec 3", "Sec 3"),
                                       ("Sec 4", "Sec 4"),
                                       ("JC 1", "JC 1"),
                                       ("JC 2", "JC 2"),
                                       ("None of the above", "None of the above")])
    is_mentor = forms.BooleanField(help_text="Do you want to be a mentor?")

    class Meta:
        model = User
        fields = ('username', 'level', 'is_mentor', 'password1', 'password2')


class CreateGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 8}))

    class Meta:
        model = Group
        fields = ("name", "description")


class PostComment(forms.ModelForm):
    text = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 100, 'rows': 10}))

    class Meta:
        model = Comment
        fields = ('text',)


class CreateClassForm(forms.ModelForm):
    name = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 10}))

    class Meta:
        model = Classes
        fields = ('name', 'description')


class CreateTimeChoice(forms.ModelForm):
    start = forms.DateTimeField()
    duration = forms.IntegerField()

    class Meta:
        model = TimeChoice
        fields = ('start', 'duration')


class CreateQuestion(forms.ModelForm):
    question = forms.CharField(max_length=240, widget=forms.Textarea(attrs={'cols': 48, 'rows': 3}))
    description = forms.CharField(max_length=5000, widget=forms.Textarea(attrs={'cols': 48, 'rows': 10}))

    class Meta:
        model = Questions
        fields = ('question', 'description')
