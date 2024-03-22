from django import forms
from anotas.models import Page, Category, Note
from django.contrib.auth.models import User
from anotas.models import UserProfile
from markdownx.fields import MarkdownxFormField

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)


    class Meta:

        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        slug = forms.CharField(widget=forms.HiddenInput(), required=False)
        fields = ('picture',)

class NoteForm(forms.ModelForm):
    noteTitle = forms.CharField(max_length=128, help_text="Note title:  ")
    subject = forms.CharField(max_length=128, help_text="Note subject")
    isPrivate = forms.BooleanField(help_text="Is Private", required=False)
    fileName = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    content = forms.Textarea()

    class Meta:
        model = Note
        fields = ['noteTitle', 'subject', 'isPrivate', 'fileName', 'content']
        
class EditForm(forms.ModelForm):
    content = forms.Textarea()
    class Meta:
        model = Note
        fields = ["content"]

