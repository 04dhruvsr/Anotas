import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anotas_project.settings')
django.setup()

from django.contrib.auth.models import User
from anotas.models import Subject, UserProfile, Note
from django.template.defaultfilters import slugify
from django.utils import timezone as tz

def populate_database():
    # Sample data dictionaries for each model
    subjects_data = [
        {"name": "Mathematicas", "views": 100, "i" : 1,"subject":None},
        {"name": "Physicas", "views": 150, "i": 2,"subject":None},
        {"name": "Biologies", "views": 200, "i": 3,"subject":None}
    ]

    users_data = [
        {"username": "user1", "email": "user1@example.com", "password": "password1","user":None},
        {"username": "user2", "email": "user2@example.com", "password": "password2","user":None},
        {"username": "user3", "email": "user3@example.com", "password": "password3","user":None},
    ]

    notes_data = [
        {"noteTitle": "Note 1", "userID": 0, "subject_id": 0, "isPrivate": False},
        {"noteTitle": "Note 2", "userID": 1, "subject_id": 1, "isPrivate": True},
        {"noteTitle": "Note 3", "userID": 2, "subject_id": 2, "isPrivate": False}
    ]


    i= 0
    for subject_data in subjects_data:
        i+=1
        subject = subject_data['name']
        if not Subject.objects.filter(name=subject).exists():
            subject = Subject.objects.create(**subject_dict)
            subject.save()
            subjects[i]["subjects"] = subject




    i= 0
    for user_data in users_data:
        username = user_data['username']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(**user_dict)
            user = UserProfile.objects.create(user)
            users_data[i]["user"] = user
            i +=1


    for note_data in notes_data:
        note = Note(
        subject= subjects_data[int(note_data["subject_id"])]["subject"],
        noteTitle=note_data["noteTitle"],
        isPrivate=note_data["isPrivate"],
        userID = users_data[int(note_data["userID"])]["user"],
    )
        note.save()

# Call the function to populate the database



if __name__ == '__main__':
    print('Starting Anotas population script...')
    populate_database()
