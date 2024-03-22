from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from anotas.views import (
    home, about, show_subject, add_subject, add_note,
    register, user_login, restricted, user_logout, note_editor, user_page, copy_note
)
from anotas.models import Subject, Note, UserProfile
from anotas.forms import NoteForm, SubjectForm, UserProfileForm, UserForm
import os

class UrlTest(SimpleTestCase):
    def test_home_url(self):
        url = reverse('anotas:home')
        self.assertEqual(resolve(url).func, home)
    
    def test_about_url(self):
        url = reverse('anotas:about')
        self.assertEqual(resolve(url).func, about)

    def test_add_subject_url(self):
        url = reverse('anotas:add_subject')
        self.assertEqual(resolve(url).func, add_subject)

class HomeViewTest(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get(reverse('anotas:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anotas/home.html')

class TemplateTest(TestCase):
    def test_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'anotas/home.html')

    def test_about_template(self):
        response = self.client.get(reverse('anotas:about'))
        self.assertTemplateUsed(response, 'anotas/about.html')

    def test_login_template(self):
        response = self.client.get(reverse('anotas:login'))
        self.assertTemplateUsed(response, 'anotas/login.html')

    def test_register_template(self):
        response = self.client.get(reverse('anotas:register'))
        self.assertTemplateUsed(response, 'anotas/register.html')

class SubjectModelTest(TestCase):
    def test_subject_creation(self):
        subject = Subject.objects.create(name='Test Subject')
        self.assertEqual(subject.name, 'Test Subject')

class NoteFormTest(TestCase):
    def setUp(self):
        # Create a Subject instance for the tests
        self.subject = Subject.objects.create(name='Mathematics')

    def test_valid_form(self):
        form_data = {
            'noteTitle': 'Algebra Basics',
            'subject': self.subject.pk, 
            'isPrivate': False,
            'fileName': 'algebra_basics.txt'
        }
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        # Test if form is invalid with blank data
        form = NoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_invalid_subject(self):
        form_data = {
            'noteTitle': 'Algebra Basics',
            'subject': 'Invalid Subject', 
            'isPrivate': False,
            'fileName': 'algebra_basics.txt'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_missing_fields(self):
        form_data = {
            'noteTitle': 'Algebra Basics',
            # 'subject' field is missing intentionally
            'isPrivate': False,
            'fileName': 'algebra_basics.txt'
        }
        form = NoteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)