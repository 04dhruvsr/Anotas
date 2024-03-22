from django import forms
from django.contrib.auth.models import User
from anotas.models import Subject, Note, UserProfile
from markdownx.fields import MarkdownxFormField


# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

#     class Meta:
#         model = Page
#         exclude = ('subject',)

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         url = cleaned_data.get('url')
#         if url and not url.startswith('http://'):
#             url = f'http://{url}'
#             cleaned_data['url'] = url
#         return cleaned_data
    
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
    choices = Subject.objects.all()
    choiceText = ()
    for i in list(choices):
        print(type(Subject.objects.get(name=i)))
        choiceText = ((Subject.objects.get(name=i), i.name),) + choiceText
    print(choiceText)
    subject = forms.ChoiceField(widget=forms.Select(), choices=choiceText)
    isPrivate = forms.BooleanField(help_text="Is Private", required=False)
    
    class Meta:
        model = Note
        fields = ['noteTitle', "subject", 'isPrivate']
        
# class EditForm(forms.ModelForm):
#     content = forms.Textarea()
#     class Meta:
#         model = Note
#         fields = ["content"]
        
class SubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Subject")

    class Meta:
        model = Subject
        fields = ['name']

