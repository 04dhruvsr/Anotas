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
        model = UserProfile
        fields = ('user', 'email', 'password',)

#class UserProfileForm(forms.ModelForm):
 #   class Meta:
  #      model = UserProfile
   #     fields = ('website', 'picture',)

class NoteForm(forms.ModelForm):
    noteTitle = forms.CharField(max_length=128, help_text="Please enter the title of the note.")
    # userId = forms.(required = True)
    # subject = forms.ForeignKey(required = True)

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     self.fields['contact_name'].label = "Your name:"
    #     self.fields['contact_name'].initial = self.request.user.userID

    class Meta:
        model = Note
        # fields = ['noteTitle', 'subject', 'isPrivate', 'fileName']
        fields = ['noteTitle', 'isPrivate', 'fileName']

class SubjectForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="What subject is this for")

    class Meta:
        model = Note
        fields = ['name']
